# PAM Project: Deep Reinforcement Learning in Sonic The Hedgehog

## Introduction:
The following repository contains the source code of my PAM Project for ACECOM, it's an implementation of PPO in Sonic The Hedgehog with the objective of finishing the first zone.
OpenAI Gymnasium and Stable-Retro APIs will be used to create and train our model.

## Author:
Ángel Aarón Flores Alberca

## Requisites:
* Python 3.10
* OS: Windows 10/11, Linux, macOS

## Installation:
Follow these steps to set up correctly the virtual environment and run the model locally:

### 1. Clone this repository
```bash
git clone https://github.com/bxcowo/sonic_genesis_PPO.git
```

### 2. Create and activate virtual environment
To create venv:
```bash
python3 -m venv .venv
```
To activate venv:
- On windows
```bash
.venv\Scripts\activate
```
- On macOS and Linux
```bash
python3 -m venv .venv
```

### 3. Upgrade pip
```bash
pip install --upgrade pip
```

### 4. Install required dependencies
```bash
pip install -r requirements.txt
```

### 5. Edit and run main.py
Using the IDE of your preference you can access the structure of the project and run [main.py](main.py).
There you'll find the definition of the model build to play Sonic The Hedgehog. 

In case you'd like to modify it and experiment, I'd recommend to update some of the hyperparameters in multiples of what has already been established.
What [main.py](main.py) does is to start training the agent using 5 cores of your CPU, this can be edited, in the level defined in [metadata.json](custom_integration/SonicTheHedgehog-Genesis-Custom/metadata.json), you can change it to any of the states saved in said directory.

### 6. Testing the model
Once the agent has finished its training, there'll be 2 new files which will be used in [testing_model.py](testing_model.py).
This script will try out what the agent has learnt and export 2 .bk2 files as a result of its attempt, but only the first one is necessary.
You can also see how the model plays during the running of the script, but it'll be very quickly, so in order to see a more detailed repetition you can render it to video using said files. 

### 7. Render to video
Before rendering, it's important to do the following: for some reason when trying to integrate our custom environment using **stable-retro** doesn't work, so in order to render the model attempts in video, it's important to move the directory inside of [custom_integration](custom_integration) to [.venv/lib/python3.10/site-packages/retro/data/stable](.venv/lib/python3.10/site-packages/retro/data/stable).
Once it's done, we execute the following command:
```bash
python3 -m retro.scripts.playback_movie SonicTheHedgehog-Genesis-Custom-[Selected zone].[Selected act]-000000.bk2
```

### Important note:
Inside of [custom_integration](custom_integration) there'll be the definition of the custom environment used for the training with the following files:
* **contest.json**: Declares how are the reward function and done condition being taken. 
* **data.json**: List of variables in RAM and their respective memory addresses and types to be interpreted correctly.
* **metadata.json**: Defines what state is the agent playing on.
* **script.lua**: Mini script made in lua that defines the reward function and the done condition.

If you want to modify something related to the custom environment, modify [script.lua](custom_integration/SonicTheHedgehog-Genesis-Custom/script.lua) or [metadata.json](custom_integration/SonicTheHedgehog-Genesis-Custom/metadata.json), avoid editing the others.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
