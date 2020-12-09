# Torcs - Reinforcement-Learning
Discretized Q-Learning on Torcs ( Lane keeping assistant )

Output:
https://youtu.be/QhDOWCuL2Qw

## Introduction
In our project, we aim at tackling one of the most crucial problems of this century;
the problem of self-driving cars. We targeted the aspect of lane-keeping together with
maximizing the car's speed, and we adopted a Q-learning algorithm. We tried out four different
scenarios where we altered the hyper-parameters and the way the reward function is calculated in
an attempt to arrive at the best possible model. In this report, we present the exact algorithm used
and discuss our results, as well as possible future work. 


## SCR-Plugin
In normal cases, cars in TORCS are granted
full access of the environment information
[3][6]. However, when working with
autonomous agents, we want them to have
access only to information they gain through
their sensors, because this is the type of
information they could truly acquire if they
were in a real environment [3][6]. As a
result, we activate the Simulated Car Racing
plugin (SCR-plugin) which allows us to have
a server act as a proxy for the environment
[3][6]. Consequently, the server sends our
client the available sensory input and, in
turn, receives the desired output of the
actuators from it [3][6].

###### Download links:

- [Torcs](http://torcs.sourceforge.net/index.php?name=Sections&op=viewarticle&artid=3)
- [SCR plugin](https://cs.adelaide.edu.au/%7Eoptlog/SCR2015/software.html)

## TORCS Sensors 
| Sensor | Definition |
| ------ | ---------- |
| Angle |  Angle between the car direction and the direction of the track axis |
| CurLapTime | Time elapsed during current lap |
| Damage | Current damage of the car (the higher is the value the higher is the damage) |
| distFromStartLine | Distance of the car from the start line along the track line |
| distRaced | Distance covered by the car from the beginning of the race |
| Fuel | Current fuel level |
| Gear | Current gear: -1 is reverse 0 is neutral and the gear from 1 to 6 |
| lastLapTime |  Time to complete last lap. Opponents: Vector of 36 sensors that detects the opponent distance in meters (range is [0,100]) within a specific 10 degrees sector: each sensor covers 10 degrees, from  -π to +π  around the car |
| racePos | Position in the race with respect to other cars |
| rpm | Number of rotations per minute of the car engine |
| speedX | Speed of the car along the longitudinal axis of the car |
| speedY | Speed of the car along the transverse axis of the car |
| track | Vector of 19 range finder sensors: each sensor represents the distance between the track edge and the car. Sensors are oriented every 10 degrees from -π/2 and +π/2 in front of the car. Distance are in meters within a range of 100 meters. When the car is outside of the track (i.e. track Pos is less than -1 or greater than 1), these values are not reliable! |
| trackPos | Distance between the car and the track axis. The value is normalized w.r.t. the track width: it is 0 when the car is on the axis, -1 when the car is on the left edge of the track and +1 when it is on the right edge of the car. Values greater than 1 or smaller than -1 means that the car is outside of the track |
| wheelSpinVel |  Vector of 4 sensors representing the rotation speed of the wheels |

## TORCS Control Actions
| Action | Description |
| ------ | ----------- |
| Accel | Virtual gas pedal (0 means no gas, 1 full gas) |
| Brake | Virtual brake pedal (-1 means no brake, 1 full brake) |
| Gear | Gear value |
| Steering | Steering value: -1 and +1 means respectively full left and right, that corresponds to an angle of 0.785398 rad |
| Meta | This is meta-control command: 0 Do nothing, 1 ask competition server to restart the race |


## Procedure

**1. STATES**

It’s clear that most of the sensor readings represent car states and it is very important for control the car

The states are the speed along the track, the position on the track, the angle with respect to the track axis and five distance sensors that measure the distance to the edge of the track. Note that the track may contain a gravel trap or a bank of grass, which means that the edge of the track might be further away than the edge of the actual road. The 20◦ inputs are not taken directly from sensors 7 and 11, but computed as an average over sensors 6, 7, 8 and 10, 11, 12, respectively, to account for noise

| Sensor |	State Description |
| ------ | ----------------- |
| speedX |	Speed of the car along the longitudinal axis of the car |
| Angle |	Angle between the car direction and the direction of the track axis |
| Track pos |	Distance between the car and the track axis |
| track | Distance sensor at −40◦, −20◦, 0◦, 20◦, 40◦	Distance between the car and track [5, 7, 9, 11, 13] |



**2. Actions**

There are five action dimensions available in TORCS accelerate, brake, gear, meta and steer. Since braking is simply a negative acceleration, we shall view this as the negative side of the same dimension.

The basic controller of the SCR

| Name |	Range |	Description |
| ---- | ----- | ----------- |
| Accel |	[0,1] |	Virtual gas pedal (0 means no gas, 1 full gas) |
| Brake |	[0,1] |	Virtual brake pedal (0 means no brake, 1 full brake) |
| Gear |	 -1,0,1,2,3,4,5,6 |	Gear value |
| Steer |	[-1,1] |	Steering value: -1 and +1 means respectively full right and left |
| Meta |	0 or 1 |	This is meta-control command: 0 do nothing, 1 ask competition server to restart the race |


**3. Rewards**

Due to random actions there are good actions and bad actions, we want to achieve our target so we want to prevent the car to
- Going out of the track
- Stopping in a certain position
- Making bad actions

To calculate the rewards, we have 3 situations:

1. Car make good lane keeping
   - the reward will be positive and high if the distance was long and in general it has a continuous range from [-1,1]

2. Stop in certain position
   - the reward will be negative and equal to -1

3. The car goes out of the track
   - the reward will be negative and equal to -1 and we will restart the race



## The Game Loop

To understand how the agent works, it is important to know what the game loop looks like. Each
game tick the SCR server asks the driver to return an action by calling its drive.
The drive function consists of two parts: one that checks whether the agent is stuck or outside
the road and one that handles action selection and learning.

### The code consists of :

**1. carControl**

   It has the control functions that control the car in game, by giving it values then it parses it and sends it to the server to move the car with the given actions.

**2. carState**

   It has all the sensor values, distance from start, damage taken and everything else describes the car state.

**3. msgParser**

   It has a UDP message builder and receiver for the server-client communication. It builds the messages of the control actions and sends it to the server then receives the UDP messages from the server which is the car state.

**4. pyclient**

   It is the client code that connects to the server host given a specific port and socket and then calls the driver function which is our game loop and then uses the msgParser to transfer the UDP messages to the server




### Drive implementation

**1. CheckStuck**

This function check that the car is stuck or not, If the car's angle is larger than 45 degrees, it is considered stuck. If it is stuck for more than 25 game ticks and the traveled distance is less than 0.01m, the episode ends. Every time the agent is not stuck, the stuck timer is reset to zero.

**2. Learning Interface**

The primary function of the learning interface is to do action selection and call the update
function of the learning algorithm.
Learning interface consists of GetState, ActionSelection, RewardFunction and QtableUpdate.

### Learning Interface steps:

**1. GetState**

First, we discretize the distance sensor and speed values as follows:

- speedList = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
- distList     = [-1,0,5,10,20,30,40,50,60,70,80,90,100,120,150,200]


     We chose these values carefully to cover all possible states and we represented each of them in 4 bits of binary form as they are 16 discretized values.

     To reduce the number of bits representing the state, we used only 1 sensor out of 5 sensors in which we take the maximum, as representing all the 5 sensors we will need to represent them in 20 bits, which will make the number of states equals to 220 which is infeasible.

    Therefore, we used another 3 bits to distinguish between the maximum of the 5 sensors which gives us of total 7 bits describing the sensor values.

    Eventually, we have a total of 11 bits for the states which corresponds to 2048 possible state

    e.g. Distance sensor = 200, Maximum sensor No. is 9, Speed = 90, this is equivalent to 1001 010 1111



**2. ActionSelection**

We discretized the actions into 15 discrete values as follows:

| Steer | Accelerate(1) | Neutral(0) | Brake(-1) |
| ----- | ------------- | ---------- | --------- |
| 0.5(left) | 0 | 1 | 2 |
| 0.1(left) | 3 | 4 | 5 |
| 0 | 6 | 7 | 8 |
| -0.1(right) | 9 | 10 | 11 |
| -0.5(right) | 12 | 13 | 14 |

Action selection is based on a random number between 0 and 1
       Policy(s) = **Informed** if num < eta  **Random** if num < eta+epsilon 	 **Max action** otherwise

Every time step there is a probability  of taking a heuristic action, a probability  of taking a random action, and a probability 
of taking a greedy action (max action).

The heuristic action is more used as a guide than as a teacher.
Therefore, the random exploration is necessary to learn to improve upon the heuristic policy.
Max action is the action which has the highest Q-value in the Q-table given the current state.



**3. RewardFunction**

We have 3 different scenarios:

- If the car is stuck

It takes -2 reward and sends a meta action to restart the episode, because it is an undesirable action, therefore we make sure it never happens again

- If the car is out of track (abs(track position) > 1)

It takes -1 reward

- If the car is neither stuck or out of track

It takes a reward depending on track position, angle and travelled distance with a max value of 1



**4. QtableUpdate**

First, we check if the current state already exists in the table, if not we create it in the Q-table initialized with 0 for all actions.

Then, using the current state, the previous state, action and reward we update the Q-values of the previous state

It is possible for multiple actions to have the same value, for example when a new state is explored
and all values are unknown (and all have default value 0). Then, the agent must make a decision
based on something other than the value. It could pick an action based on some heuristic, or
simply the first action that popped up.

## References
[1] A. Davies, P. Martineau, M. Molteni, A.
Watercutter, M. Simon, E. Pao and L.
Mallonee, "What Is a Self-Driving Car? The
Complete WIRED Guide", WIRED.
[Online]. Available:
https://www.wired.com/story/guide-selfdriving-cars/. [Accessed: 18- Oct- 2018].
[2] "Learning to drive in a day.", Wayve.
[Online]. Available:
https://wayve.ai/blog/learning-to-drive-in-aday-with-reinforcement-learning.
[Accessed: 18- Oct- 2018].
[3] D. Karavolos, Q-learning with heuristic
exploration in Simulated Car Racing.
Amsgerdam: University of Amsterdam,
2013.
[4] N. Shimkin, Learning in Complex Systems -
Reinforcement Learning – Basic
Algorithms. 2011.
[5] B. Wymann and E. Espié, "torcs ›
News", Torcs.sourceforge.net, 2016.
[Online]. Available:
http://torcs.sourceforge.net/. [Accessed: 15-
Dec- 2018].
[6] A. Raafat, "A-Raafat/Torcs---ReinforcementLearning-using-Q-Learning", GitHub, 2016.
[Online]. Available: https://github.com/ARaafat/Torcs---Reinforcement-Learningusing-Q-Learning. [Accessed: 15- Dec2018].
[7] "TORCS", En.wikipedia.org, 2018. [Online].
Available:
https://en.wikipedia.org/wiki/TORCS#Com
petitions. [Accessed: 15- Dec- 2018].
[8] M. Abdou Tolba, AUTONOMOUS DRIVING
USING DEEP REINFORCEMENT
LEARNING. Cairo: Faculty of Engineering
at Cairo University, 2017.
