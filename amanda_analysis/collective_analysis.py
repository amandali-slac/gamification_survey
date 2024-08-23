import marimo

__generated_with = "0.7.2"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    return mo, np, pd


@app.cell
def __(pd):
    wed8 = pd.read_csv("/Users/amandali/projects/surveyapp/old_stuff/old_survey/participant_data/wednesday_8am_answers.csv")
    wed12 = pd.read_csv("/Users/amandali/projects/surveyapp/old_stuff/old_survey/participant_data/wednesday_12pm_answers.csv")
    wed4 = pd.read_csv("/Users/amandali/projects/surveyapp/old_stuff/old_survey/participant_data/wednesday_4pm_answers.csv")
    sat12 = pd.read_csv("/Users/amandali/projects/surveyapp/old_stuff/old_survey/participant_data/saturday_12pm_answers.csv")
    return sat12, wed12, wed4, wed8


@app.cell
def __(pd):
    reevaluation_df = pd.read_csv("/Users/amandali/projects/surveyapp/old_stuff/old_survey/wednesday_8am_12pm_4pm_reevaluation.csv")
    return reevaluation_df,


@app.cell
def __(breakdown, reevaluation_df):
    breakdown(reevaluation_df.iloc[1].tolist())
    return


@app.cell
def __(pd):
    filler_df = pd.DataFrame(columns = ["Achiever, Explorer, Socializer, Influencer"])
    return filler_df,


@app.cell
def __(breakdown, reevaluation_df):
    breakdown(reevaluation_df.iloc[0].tolist())
    return


@app.cell
def __(breakdown, filler_df, pd, reevaluation_df):
    for i in range(reevaluation_df.shape[0]):
        new_df = breakdown(reevaluation_df.iloc[i].tolist())
        filler_df = pd.concat([filler_df, new_df])
    return filler_df, i, new_df


@app.cell
def __():
    return


@app.cell
def __(pd):
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
        return (pd.DataFrame([result]))

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
    return answers_to_int, breakdown


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
