import marimo
import pandas as pd
import numpy as np
import marimo as mo
import matplotlib.pyplot as plt

def answers_to_int(answers_str, personality_class):
    '''
    :type answers_list: arr str
    :type personality_class: pandas dataframe
    :rtype: arr int

    * personality_class: first column has possible questions, each personality type represented as columns and corresponding row vals are survey answers that fit under that personality type
    '''
    result = []
    # for each question (row indexes)
    for row in range(len(answers_str)):
        # then check the values in that row, aka the possible answers to that question
        for col in range(personality_class.shape[1]):
            # if the 
            if personality_class.iloc[row, col] == answers_str[row]:
                result.append(col)

    return result


# transform list of num values into dict with personality types as keys and 
def breakdown(answers_int):
    '''
    :type answers_int: arr int
    :rtype: dataframe

    takes in a arr of integers that represent personality classes and organizes them into a dictionary with aggregates
    '''
    result = {
    "Achiever": 0,
    "Explorer": 0,
    "Socializer": 0,
    "Influencer":0
    }
    for k in range(len(answers_int)):
        if answers_int[k] == 1:
            result["Achiever"] += 1
        elif answers_int[k] == 2:
            result["Explorer"] += 1
        elif answers_int[k] == 3:
            result["Socializer"] += 1
        elif answers_int[k] == 4:
            result["Influencer"] += 1
    return pd.DataFrame([result])


def breakdown_weighted(answers_int, expert_weights):
    '''
    :type answers_int: arr int
    :type expert_weights: dict (first four columns need to be named a1, a2, a3, a4)
    :rtype: dataframe
    '''
    result = {category: 0 for category in ["Socializer", "Influencer", "Achiever", "Explorer"]}
    num_questions = len(answers_int)
    answers = []

    for i in range(num_questions):
        answers.append(f"a{answers_int[i]}")

    for q in range(num_questions):
        answer_id = q * 4
        for looper in range(4):
            personality_type = expert_weights.loc[answer_id, "Categories"]
            personality_weight = expert_weights.loc[answer_id, answers[q]]
            result[personality_type] += personality_weight
            answer_id += 1

    return pd.DataFrame([result])


### graph calculation from reegine
def plot(results):
    
    # personality dataframe
    

    # locus
    achiever = results["Achiever"]
    explorer = results["Explorer"]
    socializer = results["Socializer"]
    influencer = results["Influencer"]
    
    _total = (
        achiever
        + explorer
        + socializer
        + influencer
    )
    locus = pd.DataFrame(
        {
            "x": (
                achiever
                + explorer
                - socializer
                - influencer
            )
            / _total,
            "y": (
                achiever
                - explorer
                - socializer
                + influencer
            )
            / _total,
        }
    )
    locus["count"] = 1
    
    
    locus.plot.scatter(
        x="x",
        y="y",
        s= locus["count"]/len(locus)*1000,
        color="lightblue",
        title=f"Personality locus (N={len(locus)})",
    )
    
    plt.plot(
        locus["x"].mean(),
        locus["y"].mean(),
        "xg",
        markersize=10,
        label="locus",
    )

    plt.plot([-1, 1], [0, 0], "k", linewidth=0.5)
    plt.plot([0, 0], [-1, 1], "k", linewidth=0.5)
    plt.text(0.5, 0.55, "ACHIEVER", horizontalalignment="center")
    plt.text(0.5, -0.65, "EXPLORER", horizontalalignment="center")
    plt.text(-0.5, -0.65, "SOCIALIZER", horizontalalignment="center")
    plt.text(-0.5, 0.55, "INFLUENCER", horizontalalignment="center")
    plt.text(
        1.1,
        0,
        "System focus",
        rotation=90,
        verticalalignment="center",
        horizontalalignment="center",
    )
    plt.text(
        -1.1,
        0,
        "Individual focus",
        rotation=90,
        verticalalignment="center",
        horizontalalignment="center",
    )
    plt.text(
        0,
        1.1,
        "Action motive",
        verticalalignment="center",
        horizontalalignment="center",
    )
    plt.text(
        0,
        -1.1,
        "Interaction motive",
        verticalalignment="center",
        horizontalalignment="center",
    )
    plt.xlim([-1.2, 1.2])
    plt.ylim([-1.2, 1.2])
    plt.xlabel("Attention")
    plt.ylabel("Motivation")
    plt.legend(loc="upper left")

    return plt.gca()
    
