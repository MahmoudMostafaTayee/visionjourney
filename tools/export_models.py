#!/usr/bin/env python3
"""
Export small but genuine ONNX vision architectures for the Model Lab.

Each model is a real PyTorch module exported with torch.onnx, then read back with
onnx.shape_inference so the explorer shows true tensor shapes, parameter counts
and skip-connection edges.

Outputs:
    models/<id>.onnx
    models/graphs/<id>.json
    models/catalog.json

Usage: python3 tools/export_models.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import onnx
import torch
import torch.nn as nn
import torch.nn.functional as F
from onnx import shape_inference

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
GRAPHS = MODELS / "graphs"


# ---------------------------------------------------------------------------
# Architectures (deliberately small so the repository stays light)
# ---------------------------------------------------------------------------

class DemoCNN(nn.Module):
    """LeNet-5 shaped classifier for 28x28 grayscale digits."""

    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * 7 * 7, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class ResidualBlock(nn.Module):
    def __init__(self, channels: int, stride: int = 1):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        identity = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return F.relu(out + identity)


class ResNetMini(nn.Module):
    """A four-stage residual network: stem, four stages, global pool, head."""

    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2, padding=1),
        )
        self.stage1 = nn.Sequential(ResidualBlock(16), ResidualBlock(16))
        self.stage2 = nn.Sequential(ResidualBlock(16), ResidualBlock(16))
        self.stage3 = nn.Sequential(ResidualBlock(16), ResidualBlock(16))
        self.stage4 = nn.Sequential(ResidualBlock(16), ResidualBlock(16))
        self.head = nn.Linear(16, num_classes)

    def forward(self, x):
        x = self.stem(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = F.adaptive_avg_pool2d(x, 1).flatten(1)
        return self.head(x)


class TinyVit(nn.Module):
    """Patch embedding + two pre-norm transformer blocks + classifier."""

    def __init__(self, dim: int = 32, heads: int = 4, depth: int = 2, num_classes: int = 10):
        super().__init__()
        self.patch = nn.Conv2d(3, dim, 4, stride=4)  # 32x32 -> 8x8 tokens
        self.cls = nn.Parameter(torch.zeros(1, 1, dim))
        self.pos = nn.Parameter(torch.zeros(1, 65, dim))
        self.blocks = nn.ModuleList(
            [
                nn.ModuleDict(
                    {
                        "norm1": nn.LayerNorm(dim),
                        "qkv": nn.Linear(dim, dim * 3),
                        "proj": nn.Linear(dim, dim),
                        "norm2": nn.LayerNorm(dim),
                        "fc1": nn.Linear(dim, dim * 2),
                        "fc2": nn.Linear(dim * 2, dim),
                    }
                )
                for _ in range(depth)
            ]
        )
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, num_classes)
        self.dim = dim
        self.heads = heads
        self.depth = depth

    def forward(self, x):
        b = x.shape[0]
        x = self.patch(x).flatten(2).transpose(1, 2)
        cls = self.cls.expand(b, -1, -1)
        x = torch.cat([cls, x], dim=1)
        x = x + self.pos[:, : x.shape[1]]
        for block in self.blocks:
            h = block["norm1"](x)
            qkv = block["qkv"](h)
            q, k, v = qkv.chunk(3, dim=-1)
            q = q.reshape(b, -1, self.heads, self.dim // self.heads).transpose(1, 2)
            k = k.reshape(b, -1, self.heads, self.dim // self.heads).transpose(1, 2)
            v = v.reshape(b, -1, self.heads, self.dim // self.heads).transpose(1, 2)
            attn = (q @ k.transpose(-2, -1)) / (self.dim // self.heads) ** 0.5
            attn = attn.softmax(dim=-1)
            out = (attn @ v).transpose(1, 2).reshape(b, -1, self.dim)
            x = x + block["proj"](out)
            x = x + block["fc2"](F.gelu(block["fc1"](block["norm2"](x))))
        x = self.norm(x)[:, 0]
        return self.head(x)


class DoubleConv(nn.Module):
    def __init__(self, cin: int, cout: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(cin, cout, 3, padding=1, bias=False),
            nn.BatchNorm2d(cout),
            nn.ReLU(),
            nn.Conv2d(cout, cout, 3, padding=1, bias=False),
            nn.BatchNorm2d(cout),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.net(x)


class UNetMini(nn.Module):
    """Two-level U-Net: the canonical encoder–decoder with skip concatenation."""

    def __init__(self, classes: int = 3):
        super().__init__()
        self.down1 = DoubleConv(3, 16)
        self.down2 = DoubleConv(16, 32)
        self.bottleneck = DoubleConv(32, 64)
        self.up2 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.dec2 = DoubleConv(64, 32)
        self.up1 = nn.ConvTranspose2d(32, 16, 2, stride=2)
        self.dec1 = DoubleConv(32, 16)
        self.out = nn.Conv2d(16, classes, 1)

    def forward(self, x):
        d1 = self.down1(x)
        p1 = F.max_pool2d(d1, 2)
        d2 = self.down2(p1)
        p2 = F.max_pool2d(d2, 2)
        b = self.bottleneck(p2)
        u2 = self.up2(b)
        u2 = self.dec2(torch.cat([u2, d2], dim=1))
        u1 = self.up1(u2)
        u1 = self.dec1(torch.cat([u1, d1], dim=1))
        return self.out(u1)


class InvertedResidual(nn.Module):
    """MobileNetV2 inverted residual: expand 1x1, depthwise 3x3, project 1x1."""

    def __init__(self, cin: int, cout: int, expand: int = 4, stride: int = 1):
        super().__init__()
        hidden = cin * expand
        self.use_residual = stride == 1 and cin == cout
        self.expand = nn.Sequential(nn.Conv2d(cin, hidden, 1), nn.ReLU6())
        self.depthwise = nn.Sequential(
            nn.Conv2d(hidden, hidden, 3, stride=stride, padding=1, groups=hidden), nn.ReLU6()
        )
        self.project = nn.Conv2d(hidden, cout, 1)

    def forward(self, x):
        out = self.project(self.depthwise(self.expand(x)))
        return out + x if self.use_residual else out


class MobileBlockStack(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.stem = nn.Sequential(nn.Conv2d(3, 16, 3, stride=2, padding=1), nn.ReLU6())
        self.blocks = nn.Sequential(
            InvertedResidual(16, 16, 4, 1),
            InvertedResidual(16, 24, 4, 2),
            InvertedResidual(24, 24, 4, 1),
            InvertedResidual(24, 32, 4, 2),
        )
        self.head = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, num_classes))

    def forward(self, x):
        return self.head(self.blocks(self.stem(x)))


MODELS_SPEC = [
    {
        "id": "demo-cnn",
        "name": "Demo CNN (LeNet shape)",
        "task": "10-class classification · 1×28×28",
        "module": DemoCNN,
        "input": (1, 1, 28, 28),
        "stages": [(r"features\.0", "conv1"), (r"features\.3", "conv2"), (r"classifier\.1", "fc1"), (r"classifier\.3", "logits")],
        "note": "Two convolutions, two pools, two linear layers — the smallest complete vision graph.",
    },
    {
        "id": "resnet-mini",
        "name": "ResNet-Mini",
        "task": "Residual classification · 3×64×64",
        "module": ResNetMini,
        "input": (1, 3, 64, 64),
        "stages": [(r"stem", "stem"), (r"stage1", "stage 1"), (r"stage2", "stage 2"), (r"stage3", "stage 3"), (r"stage4", "stage 4"), (r"head", "head")],
        "note": "Identity shortcuts make the graph a DAG, not a chain: follow the Add nodes.",
    },
    {
        "id": "vit-tiny",
        "name": "Tiny ViT",
        "task": "Patch-transformer classification · 3×32×32",
        "module": TinyVit,
        "input": (1, 3, 32, 32),
        "stages": [(r"patch", "patch embed"), (r"blocks\.0", "block 1"), (r"blocks\.1", "block 2"), (r"norm", "final norm"), (r"head", "classifier")],
        "note": "Attention is just MatMul → Softmax → MatMul: find the 4×65×65 score tensors.",
    },
    {
        "id": "unet-mini",
        "name": "U-Net Mini",
        "task": "Semantic segmentation · 3×64×64",
        "module": UNetMini,
        "input": (1, 3, 64, 64),
        "stages": [(r"down1", "encoder 1"), (r"down2", "encoder 2"), (r"bottleneck", "bottleneck"), (r"up2|dec2", "decoder 2"), (r"up1|dec1|out", "decoder 1")],
        "note": "Skip concatenations carry high-resolution detail across the bottleneck.",
    },
    {
        "id": "mobilenet-block",
        "name": "Mobile Inverted Residual",
        "task": "Efficient classification · 3×64×64",
        "module": MobileBlockStack,
        "input": (1, 3, 64, 64),
        "stages": [(r"stem", "stem"), (r"blocks\.0", "block 1 · 1×16"), (r"blocks\.1", "block 2 · 2×24"), (r"blocks\.2", "block 3 · 1×24"), (r"blocks\.3", "block 4 · 2×32"), (r"head", "head")],
        "note": "Depthwise convolution (groups = channels) trades FLOPs for memory traffic.",
    },
]


# ---------------------------------------------------------------------------
# Export + graph extraction
# ---------------------------------------------------------------------------

def stage_of(name: str, rules: list[tuple[str, str]]) -> str:
    for pattern, label in rules:
        if re.search(pattern, name):
            return label
    return "other"


def initials(model: onnx.ModelProto) -> dict[str, int]:
    sizes = {}
    for init in model.graph.initializer:
        count = 1
        for d in init.dims:
            count *= d
        sizes[init.name] = count
    return sizes


def dims_of(value_info) -> list:
    shape = []
    for d in value_info.type.tensor_type.shape.dim:
        if d.dim_value:
            shape.append(d.dim_value)
        elif d.dim_param:
            shape.append(d.dim_param)
        else:
            shape.append("?")
    return shape


def export(spec: dict) -> dict:
    torch.manual_seed(0)
    model = spec["module"]()
    model.eval()
    dummy = torch.randn(*spec["input"])

    onnx_path = MODELS / f"{spec['id']}.onnx"
    torch.onnx.export(
        model,
        dummy,
        str(onnx_path),
        input_names=["input"],
        output_names=["logits"],
        opset_version=17,
        do_constant_folding=False,
        dynamo=False,
    )

    proto = onnx.load(str(onnx_path))
    inferred = shape_inference.infer_shapes(proto)
    shapes = {vi.name: dims_of(vi) for vi in list(inferred.graph.value_info) + list(inferred.graph.output) + list(inferred.graph.input)}
    params_by_tensor = initials(proto)

    producer = {}
    for i, node in enumerate(proto.graph.node):
        for out in node.output:
            producer[out] = i

    nodes = []
    edges = []
    for i, node in enumerate(proto.graph.node):
        for inp in node.input:
            if inp in producer and producer[inp] != i:
                edge = [producer[inp], i]
                if edge not in edges:
                    edges.append(edge)

        attrs = {}
        for attr in node.attribute:
            if attr.type == onnx.AttributeProto.INT:
                attrs[attr.name] = attr.i
            elif attr.type == onnx.AttributeProto.FLOAT:
                attrs[attr.name] = round(attr.f, 4)
            elif attr.type == onnx.AttributeProto.INTS:
                attrs[attr.name] = list(attr.ints)
            elif attr.type == onnx.AttributeProto.STRING:
                attrs[attr.name] = attr.s.decode()
        param_count = sum(params_by_tensor.get(inp, 0) for inp in node.input)
        nodes.append(
            {
                "op": node.op_type,
                "name": node.name or f"{node.op_type}_{i}",
                "out": shapes.get(node.output[0], []),
                "params": param_count,
                "attrs": attrs,
                "stage": stage_of(node.name or "", spec["stages"]),
            }
        )

    total_params = sum(p.numel() for p in model.parameters())
    graph = {
        "id": spec["id"],
        "name": spec["name"],
        "file": onnx_path.name,
        "params": total_params,
        "input": {"name": "input", "shape": list(spec["input"])},
        "nodes": nodes,
        "edges": edges,
        "note": spec["note"],
    }
    (GRAPHS / f"{spec['id']}.json").write_text(json.dumps(graph, separators=(",", ":")), encoding="utf-8")

    size_kb = onnx_path.stat().st_size / 1024
    size = f"{size_kb / 1024:.1f} MB" if size_kb > 1024 else f"{size_kb:.0f} KB"
    return {
        "id": spec["id"],
        "name": spec["name"],
        "task": spec["task"],
        "params": f"{total_params / 1e3:.1f}K" if total_params < 1e6 else f"{total_params / 1e6:.2f}M",
        "size": size,
        "file": onnx_path.name,
        "note": spec["note"],
        "nodes": len(nodes),
    }


def main() -> int:
    MODELS.mkdir(exist_ok=True)
    GRAPHS.mkdir(exist_ok=True)
    catalog = {"models": [export(spec) for spec in MODELS_SPEC]}
    (MODELS / "catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    for m in catalog["models"]:
        print(f"{m['id']:<18} {m['nodes']:>3} nodes  {m['params']:>8} params  {m['size']:>8}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
