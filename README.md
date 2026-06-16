# Satellite simulation

## Introduction

This project was made as my and my friend's first degree for Computer Science final project.

In this project, we created a visualization of earth as a simple sphere, and took starlink's TLE data from 2024 (when we were creating it) and we visualized the satellites around earth.
Then we went on and pinpointed locations on earth, and we looked for the shortest path for a light signal to travel along the satellites to create a line of sight between the two ground stations.

![New York to Tel Hai College](/single_frame.jpg)

As you can see, in this photo, we can see how the line follows the curvature of the earth, as opposed to being just a straight line.
This 'signal' passes through the satellites.

## Running

This project uses Godot3 with the python module. This is because we didn't want to spend time learning a new scripting language for the project, namely GDScript.
This allowed us to focus on developing our own code while being able to use Python libraries for handling complex math like sgp4.
Unfortunately, the MacOS Godot3 runtime didn't work with the addons for some reason, so we developed it on Linux.

So to run this, you will need to:
1. Clone the repository and open it through Godot3
<!-- 2. Install the Godot3 python runtime -->
<!-- 3. Manually install sgp4 and dijkstar libraries to the relevant directory -->
<!--     In my case this directory was `addons/pythonscript/x11-64/include/python3.8` -->
2. The pythonscript plugin along with the sgp4 and dijkstar plugins should already be available. Just press play and wait for the graph to setup (this takes around 40 seconds for a frame)

## What this project is NOT

This project does not try to simulate light travel time through the atmosphere, so we don't see any curved light rays.

This project does not compensate precisely for any mountains or elevation changes on earth.

This project does not try to create a network of satellites each acting as their own router.

## Limitations

The runtime is very slow. (About 40 seconds per frame)
There are several improvements that can be done about that, but they will not be implemented yet since I think my time is better spent elsewhere.

The line of sight calculation between the satellites and between the ground stations are very rough.
I preferred to just set the maximum distance that any two lowest satellites can see each other and go with it.
This means that higher up satellites that can see each other, may not see each other in this implementation.
This was done primarily to save runtime, since a simple distance calculation is much quicker than any other calculation.
I think that if this calculation was made properly the runtime would have increased dramatically.

## Credits

This project was made by Daniel Kusai and Tomer Gueta under the directive of Prof. Shlomo Houri at Tel-Hai College
