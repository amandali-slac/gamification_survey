import marimo

__generated_with = "0.7.2"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(r"# Survey Demo")
    return


@app.cell
def __():
    # imports
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, pd, plt


@app.cell
def __(pd):
    # files

    # list of questions as columns with selections as rows. the number of columns should be = to the number of questions in the survey
    behavioral_questions = pd.read_csv('https://raw.githubusercontent.com/amandali-slac/gamification_survey/main/data/behavioral_questions_demo.csv')

    # expert weights from validation set
    expert_weights = pd.read_csv('https://raw.githubusercontent.com/amandali-slac/gamification_survey/main/data/expert_weights.csv')

    # personality type classes
    personality_class = pd.read_csv('https://raw.githubusercontent.com/amandali-slac/gamification_survey/main/data/classification_str.csv')
    return behavioral_questions, expert_weights, personality_class


@app.cell
def __(mo):
    # descriptors
    sentence_start = mo.md(f"This is a demo for the gamification archetypes behavioral survey. It has been modified for general audiences. To begin the survey, click the button below.").center()
    sentence_survey = mo.md(f"You are required to answer all questions. Note: There are no correct or incorrect answers.").center()
    sentence_results = mo.md(f" Thank you for your time! Your results are below.").center()

    # buttons (initialized to false, turns to true once clicked)
    start_survey = mo.ui.button(label="_start_", value=False, on_click=lambda value: True, kind="success")
    submit_survey = mo.ui.button(label="_submit_", value=False, on_click=lambda value: True, kind="warn")
    return (
        sentence_results,
        sentence_start,
        sentence_survey,
        start_survey,
        submit_survey,
    )


@app.cell
def __():
    ### landing page
    return


@app.cell
def __(mo, sentence_start, start_survey):
    mo.vstack(
        [sentence_start,
        start_survey],
        align="center",
        justify="center"
    ) if (start_survey.value == False) else None
    return


@app.cell
def __():
    ### survey page
    return


@app.cell
def __(
    behavioral_questions_list,
    mo,
    sentence_survey,
    start_survey,
    submit_survey,
):
    # displaying survey form in vertical form
    behavioral_list = mo.vstack(behavioral_questions_list)
    mo.vstack(
            [sentence_survey,
             behavioral_list, 
             mo.hstack([submit_survey], justify = "end")
            ]
    ) if (start_survey.value and submit_survey.value == False) else None
    return behavioral_list,


@app.cell
def __(behavioral_questions, mo):
    ### behavioral questions

    # utilize a loop and dictionary so that the number of questions in the survey can be changed with ease in the csv, without hard-coding
    # the questions dict stores values as marimo groups, which we can access answers from later using .value

    # creating a dictionary to store questions/selections as radiogroups
    behavioral_questions_dict = {} 
    # number of columns, also the same as number of questions
    num_questions_behavioral = behavioral_questions.shape[1]

    # loop to create dictionary that stores radio elements in dictionary 
    for i in range(num_questions_behavioral): 
        # key: "question1", "question2", ..., 
        # value: answer selection radiogroup
        behavioral_questions_dict[f"question_{i + 1}"] = mo.ui.radio.from_series(behavioral_questions.iloc[:, i])

    behavioral_questions_dict = mo.ui.dictionary(behavioral_questions_dict)

    # list of radiogroup questions
    behavioral_questions_list = list(behavioral_questions_dict.values())
    return (
        behavioral_questions_dict,
        behavioral_questions_list,
        i,
        num_questions_behavioral,
    )


@app.cell
def __(behavioral_questions):
    num_questions = behavioral_questions.shape[1]
    return num_questions,


@app.cell
def __(answers_to_int, behavioral_answers_list, personality_class):
    behavioral_answers_int = answers_to_int(behavioral_answers_list, personality_class)
    return behavioral_answers_int,


@app.cell
def __(behavioral_questions_dict, num_questions):
    behavioral_answers_list = []
    for j in range(num_questions):
        behavioral_answers_list.append(behavioral_questions_dict.get(f"question_{j+1}").value)
    return behavioral_answers_list, j


@app.cell
def __():
    ### third page
    return


@app.cell
def __(descript_text, graphs, mo, sentence_results, submit_survey):
    mo.vstack(
        [sentence_results,
        graphs,
        descript_text]
    ).center() if (submit_survey.value) else None
    return


@app.cell
def __(
    behavioral_answers_int,
    breakdown,
    breakdown_weighted,
    expert_weights,
    mo,
    plot,
):
    breakdown_normal = breakdown(behavioral_answers_int)
    breakdown_validated = breakdown_weighted(behavioral_answers_int, expert_weights)
    graphs = mo.ui.tabs(
        {
            "**Pure Personality**": plot(breakdown_normal),
            "**Personality with Validator Weights**": plot(breakdown_validated),
        }
    ).center()
    return breakdown_normal, breakdown_validated, graphs


@app.cell
def __(breakdown_normal, mo):
    # sorted dictionary of personality from normal breakdown
    _descript_dict = {"Achiever": (breakdown_normal.iloc[0, 0]/8 *100), "Explorer" : (breakdown_normal.iloc[0, 1]/8 *100), "Socializer": (breakdown_normal.iloc[0, 2]/8 *100), "Influencer": (breakdown_normal.iloc[0, 3]/8 *100)}
    descript_dict = dict(sorted(_descript_dict.items(), key=lambda item: item[1], reverse=True))

    # array format of text for easy input into mo stack
    descript_arr = []
    for key, value in descript_dict.items():
        descript_arr.append(mo.md(f"{key}: {value}%"))

    # description of personality
    descript_text = mo.vstack(
        [
        mo.md("_Your personality breakdown is:_"),
        mo.md(f"**{descript_arr[0]}**"),
        mo.md(f"{descript_arr[1]}"),
        mo.md(f"{descript_arr[2]}"),
        mo.md(f"{descript_arr[3]}")
        ]
    )
    return descript_arr, descript_dict, descript_text, key, value


@app.cell
def __():
    ### functions
    return


@app.cell
def __(pd, plt):
    # tranform a list of participant answers to num values that represent personality types
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

    # transform 
    def breakdown_weighted(answers_int, expert_weights):
        '''
        :type answers_int: arr int
        :type expert_weights: dict (first four columns need to be named a1, a2, a3, a4)
        :rtype: dataframe
        '''
        result = {category: 0 for category in ["Socializer", "Influencer", "Achiever", "Explorer"]}
        num_questions = len(answers_int)
        answers = []

        # transforming answers list into "a1", "a2", ..., for csv readability
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
    return answers_to_int, breakdown, breakdown_weighted, plot


if __name__ == "__main__":
    app.run()
