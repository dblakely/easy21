# Easy 21

This is a solution to the "Easy 21" assignment from David Silver's [reinforcement learning course](https://www.davidsilver.uk/teaching/). See "assignment.pdf" in this repo for a full explanation of the task.

## Installation

```bash
pip install -r requirements.txt
```

## Demo Environment

```
python demo_environment.py
```

## Run Tests

```
python -m unittest discover tests
```

## Monte Carlo Control

```bash
python run.py --algo mc --max_episodes 100000 --N0 100
```
