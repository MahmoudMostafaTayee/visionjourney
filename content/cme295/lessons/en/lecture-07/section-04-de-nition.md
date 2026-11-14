---
lesson_id: section-04-de-nition
course_id: lecture-07
lang: en
order_index: 4
title: Deﬁnition
description: 'Slides 82–109 of lecture 7: 14 slides from the original deck.'
meta_title: Deﬁnition — Lecture 7
meta_description: Slide-by-slide walkthrough of Deﬁnition, lecture 7.
meta_keywords: Deﬁnition, lecture 7, slides
---

## Deﬁnition

:::slide{src="../../slides/lecture-07/slide-082.webp" n="82"} Deﬁnition

- "Tool calling [...] allows autonomous systems
- to complete complex tasks by dynamically
- accessing and [may act] upon external
- resources."
- " Tool calling overview ", IBM.
:::

:::slide{src="../../slides/lecture-07/slide-085.webp" n="85"} Real-life example

- Sorry, I don't know
- LLM as we've
- Find a bear near me! LLM which bears are near
- known it so far
- you.
- <function API>
- LLM with tools LLM ?
- Find a bear near me!
:::

:::slide{src="../../slides/lecture-07/slide-087.webp" n="87"} Real-life example

- ﬁnd_teddy_bear.py
- from dataclasses import dataclass # Extract coordinates from API response
- from geopy.distance import geodesic bear_lat, bear_lon = closest_teddy_bear[ "coords" ]
- import requests
- # Compute distance to the bear using geopy (returns distance in meters)
- @dataclass distance = geodesic((user_lat, user_lon), (bear_lat, bear_lon)).meters
- class TeddyBearInfo :
- name: str return TeddyBearInfo (
- distance_meters: float name=closest_teddy_bear[ "name" ],
- mood: str distance_meters=round(distance, 2),
- message: str mood=closest_teddy_bear[ "mood" ],
- message= f" {closest_teddy_bear[ 'name' ] } is {closest_teddy_bear[ 'mood' ]} "
- def find_teddy_bear(location: tuple [ float , float ]) -> TeddyBearInfo : f"and only { round (distance, 2)} meters away!"
- """ )
- Finds the nearest teddy bear to the given GPS coordinates.
- Parameters:
- location: A (latitude, longitude) pair representing the user's current
- location.
- has a descriptive,
- Returns:
- TeddyBearInfo: Information about the nearest teddy bear found. well-documented API
- """
- # Call API to get the closest teddy bear
- user_lat, user_lon = location
- api_url = "https://api.to.teddy.bears.com/v1/closest"
- try:
- response = requests.get(
- api_url,
- params={ "latitude" : user_lat, "longitude" : user_lon},
- timeout=5
- response.raise_for_status()
- closest_teddy_bear = response.json()
- except requests.RequestException as e :
- raise RuntimeError ( f"Failed to fetch teddy bear data from API: {e} " )
:::

:::slide{src="../../slides/lecture-07/slide-088.webp" n="88"} Real-life example

- ﬁnd_teddy_bear.py
- from dataclasses import dataclass # Extract coordinates from API response
- from geopy.distance import geodesic bear_lat, bear_lon = closest_teddy_bear[ "coords" ]
- import requests
- # Compute distance to the bear using geopy (returns distance in meters)
- @dataclass distance = geodesic((user_lat, user_lon), (bear_lat, bear_lon)).meters
- class TeddyBearInfo :
- name: str return TeddyBearInfo (
- distance_meters: float name=closest_teddy_bear[ "name" ],
- mood: str distance_meters=round(distance, 2),
- message: str mood=closest_teddy_bear[ "mood" ],
- message= f" {closest_teddy_bear[ 'name' ] } is {closest_teddy_bear[ 'mood' ]} "
- def find_teddy_bear(location: tuple [ float , float ]) -> TeddyBearInfo : f"and only { round (distance, 2)} meters away!"
- """ )
- Finds the nearest teddy bear to the given GPS coordinates.
- Parameters:
- location: A (latitude, longitude) pair representing the user's current
- location.
- Returns:
- TeddyBearInfo: Information about the nearest teddy bear found.
- """
- # Call API to get the closest teddy bear
- user_lat, user_lon = location
- api_url = "https://api.to.teddy.bears.com/v1/closest"
- try: (optional) has some
- response = requests.get(
- api_url, backend call
- params={ "latitude" : user_lat, "longitude" : user_lon},
- timeout=5
- response.raise_for_status()
- closest_teddy_bear = response.json()
- except requests.RequestException as e :
- raise RuntimeError ( f"Failed to fetch teddy bear data from API: {e} " )
:::

:::slide{src="../../slides/lecture-07/slide-089.webp" n="89"} Real-life example

- ﬁnd_teddy_bear.py
- from dataclasses import dataclass # Extract coordinates from API response
- from geopy.distance import geodesic bear_lat, bear_lon = closest_teddy_bear[ "coords" ]
- import requests
- # Compute distance to the bear using geopy (returns distance in meters)
- @dataclass distance = geodesic((user_lat, user_lon), (bear_lat, bear_lon)).meters
- class TeddyBearInfo :
- name: str return TeddyBearInfo (
- distance_meters: float name=closest_teddy_bear[ "name" ],
- mood: str distance_meters=round(distance, 2),
- message: str mood=closest_teddy_bear[ "mood" ],
- message= f" {closest_teddy_bear[ 'name' ] } is {closest_teddy_bear[ 'mood' ]} "
- def find_teddy_bear(location: tuple [ float , float ]) -> TeddyBearInfo : f"and only { round (distance, 2)} meters away!"
- """ )
- Finds the nearest teddy bear to the given GPS coordinates.
- Parameters:
- location: A (latitude, longitude) pair representing the user's current
- location.
- returns some info
- Returns:
- TeddyBearInfo: Information about the nearest teddy bear found.
- """
- # Call API to get the closest teddy bear
- user_lat, user_lon = location
- api_url = "https://api.to.teddy.bears.com/v1/closest"
- try:
- response = requests.get(
- api_url,
- params={ "latitude" : user_lat, "longitude" : user_lon},
- timeout=5
- response.raise_for_status()
- closest_teddy_bear = response.json()
- except requests.RequestException as e :
- raise RuntimeError ( f"Failed to fetch teddy bear data from API: {e} " )
:::

:::slide{src="../../slides/lecture-07/slide-093.webp" n="93"} How it works

- 1. Let LLM ﬁnd argument for relevant function call
- <function API> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- 2. Make function call
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- 3. Let LLM deduce conclusion based on results
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-07/slide-097.webp" n="97"} Teach a model to use a tool

- <function API>
- Method 1: via training
- Find a bear near me!
- conversation
- history so far
- LLM
- <function API>
- location = (37.42,-122.17)
- Find a bear near me!
- with find_teddy_bear ()
- Backend
- location = (37.42,-122.17) {" name ": " Teddy ", … }
- with find_teddy_bear ()
- Tool prediction response
- desired
- prediction Response generation
:::

:::slide{src="../../slides/lecture-07/slide-098.webp" n="98"} Teach a model to use a tool

- <function API>
- <function API>
- <function API> Find a bear in Paris!
- Method 1: via training Find a bear near me!
- Find a bear near me!
- LLM
- <function API> LLM
- <function API> LLM
- <function API> location = (48.86,2.35)
- Find a bear in Paris! location = (37.42,-122.17)
- Find a bear near me! location = (37.42,-122.17) with find_teddy_bear ()
- Find a bear near me! with find_teddy_bear ()
- with find_teddy_bear ()
- Backend
- Backend
- Backend
- location = (48.86,2.35) {" name ": " Ours ", … }
- location = (37.42,-122.17) {" name ": " Teddy ", … }
- location = (37.42,-122.17) with find_teddy_bear () {" name ": " Teddy ", … }
- with find_teddy_bear ()
- with find_teddy_bear ()
- response
- response
- Tool prediction response
- Response generation
:::

:::slide{src="../../slides/lecture-07/slide-101.webp" n="101"} Teach a model to use a tool

- Method 1: via training
- Method 2: via prompting how to write such a
- description?
- <function API> + <detailed explanation on how to use it>
- Find a bear near me!
- Use SFT pairs as evaluation + use a powerful reasoning model
- One way:
- to write it for you!
:::

:::slide{src="../../slides/lecture-07/slide-102.webp" n="102"} Examples of common use cases

- Information
- Web/database search
- Weather, stocks, and any other tracker
- Codebase
- Computation
- Calculator ...and many more!
- Code execution (often in Python)
- Action
- Send emails/messages and other in-computer action
- anything else within the domain of an assistant
:::

:::slide{src="../../slides/lecture-07/slide-103.webp" n="103"} In practice: many tools

- def find_teddy_bear( def hug_teddy_bear(
- def check_teddy_mood(
- location: tuple [ float , recipient: TeddyBear,
- name: TeddyBear
- float ] intensity: str = "warm"
- ) -> TeddyMood:
- ) -> TeddyBearInfo: ) -> HugResponse:
- # ...
- # ... # ...
- def schedule_playdate(
- def send_teddy_gift( def send_message(
- host: TeddyBear,
- recipient: TeddyBear, recipient: TeddyBear,
- guest: TeddyBear,
- gift: str = "poetry book" message: str
- time: datetime
- ) -> GiftResponse: ) -> MessageResponse:
- ) -> Confirmation:
- # ... # ...
- # ...
:::

:::slide{src="../../slides/lecture-07/slide-104.webp" n="104"} In practice: many tools

- <function API> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- < list of function API s > location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
:::

:::slide{src="../../slides/lecture-07/slide-106.webp" n="106"} Tools summary

- Beneﬁts.
- LLMs just became way more useful!
- They can also interact with the real world
- Overcomes "knowledge cutoﬀ" limitation
- Challenges.
- More tools = decrease performance
- Finite context length: not scalable
- Many tools to deﬁne. Lots of work.
- " Automatic Tool Selection to Reduce Large Language Model Latency ", Robert et al., 2024.
:::

:::slide{src="../../slides/lecture-07/slide-109.webp" n="109"} Tool selection

- Goal. Both reduce latency and improve performance
- 1 Router List of selected tools
- Find a bear near me!
- < selected function APIs>
- 2 LLM ...
- Find a bear near me!
- " Automatic Tool Selection to Reduce Large Language Model Latency ", Robert et al., 2024.
:::
