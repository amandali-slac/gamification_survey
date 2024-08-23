import marimo

__generated_with = "0.7.2"
app = marimo.App()


@app.cell
def __(mo):
    mo.md("# Survey Prototype")
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
def __():
    import importlib
    import my_functions as util
    return importlib, util


@app.cell
def __(pd):
    # files

    # list of questions as columns with selections as rows. the number of columns should be = to the number of questions in the survey
    behavioral_questions = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/questions/behavioral_questions.csv')
    more_info = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/questions/more_info.csv')
    preferred_activity = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/questions/preferred_activity.csv')
    all_questions = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/questions/all_questions.csv')

    # expert weights from validation set
    expert_weights = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/expert_weights.csv')

    # personality type classes
    personality_class = pd.read_csv('/Users/amandali/projects/surveyapp/amanda_analysis/form_data/classification_str.csv')
    return (
        all_questions,
        behavioral_questions,
        expert_weights,
        more_info,
        personality_class,
        preferred_activity,
    )


@app.cell
def __():
    ### some variables
    return


@app.cell
def __(mo):
    # descriptors
    sentence_access = mo.md(f"Hello, we are interested in distinguishing between participant types based on survey questions. Please start by entering the survey access code.").center()
    sentence_survey = mo.md(f"You are required to answer all questions. Note: There are no correct or incorrect answers.").center()
    sentence_results = mo.md(f" Thank you for your time! Your results are below").center()

    # buttons (initialized to false, turns to true once clicked)
    submit_access = mo.ui.button(label="_submit_", value=False, on_click=lambda value: True)
    submit_survey = mo.ui.button(label="_submit_", value=False, on_click=lambda value: True)
    return (
        sentence_access,
        sentence_results,
        sentence_survey,
        submit_access,
        submit_survey,
    )


@app.cell
def __():
    # participant data (row) to be sent to backend database
    #access_arr = code.value
    #form_arr = behavioral_answers_list
    #participant_obs = np.concatenate((access_arr, form_arr))
    return


@app.cell
def __():
    # behavioral answers used in personality calculations on last page
    #behavioral_answers_int = util.answers_to_int(behavioral_answers_list, personality_class)
    return


@app.cell
def __(behavioral_questions_dict, num_questions):
    # list of answers that the participant selects
    behavioral_answers_list = []
    for j in range(num_questions):
        behavioral_answers_list.append(behavioral_questions_dict.get(f"question_{j+1}").value)
    return behavioral_answers_list, j


@app.cell
def __():
    # need one more column at the end of database that is true/false based on whether their behavioral dominant personality matches the selection of validation question
    # make survey questions so that you can only submit once all questions are selected
    return


@app.cell
def __():
    ### first page: access code
    return


@app.cell
def __(mo):
    # prolific code address input; array
    code_placeholder = mo.ui.text(placeholder="ABCXYZ")
    code = mo.ui.array([code_placeholder], label = "Start by entering your Prolific code:")
    return code, code_placeholder


@app.cell
def __(code, mo, sentence_access, submit_access):
    # vert stack with description, access code, and submit button
    access_stack = mo.hstack(
        [mo.as_html(code), 
         submit_access
        ]
    ) 
    mo.vstack(
        [sentence_access,
         access_stack
        ]
    ) if (submit_access.value == False) else None

    # submit button shows up initially, then disappears along with hstack once clicked
    return access_stack,


@app.cell
def __():
    ### second page: survey questions
    return


@app.cell
def __(
    behavioral_questions_list,
    behavioral_subtitle,
    mo,
    sentence_survey,
    submit_access,
    submit_survey,
):
    # displaying survey form in vertical form
    behavioral_list = mo.vstack(behavioral_questions_list)
    mo.vstack(
            [sentence_survey,
             behavioral_subtitle,
             behavioral_list, 
             mo.hstack([submit_survey], justify = "end")
            ]
    ) if (submit_access.value and submit_survey.value == False) else None
    return behavioral_list,


@app.cell
def __(mo):
    behavioral_subtitle = mo.md("###**Behavioral questions**")
    more_info_subtitle = mo.md("###**More about yourself**")
    preferred_subtitle = mo.md("###**Preferred activity**")
    return behavioral_subtitle, more_info_subtitle, preferred_subtitle


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
def __(mo):
    def survey_generator(question_bank):
        '''
        :type question_bank: pandas df
        :rtype: dict
        '''
        return_dict = {}
        num_questions = question_bank.shape[1]

        for i in range(num_questions):
            # multiple choice questions
            if len(question_bank.iloc[:, i]) > 2 and len(question_bank.iloc[:, i]) < 10:
                return_dict[f"question_{i + 1}"] = mo.ui.radio.from_series(question_bank.iloc[:, i])
            # slider questions
            elif len(question_bank.iloc[:, i]) == 2:
                return_dict[f"question_{i + 1}"] = mo.ui.slider(question_bank.iloc[0, i], question_bank.iloc[1, i])
            # dropdown questions
            elif len(question_bank.iloc[:, i]) > 10:
                return_dict[f"question_{i + 1}"] = mo.ui.dropdown.from_series(question_bank.iloc[:, i])

        return mo.ui.dictionary(return_dict)
    return survey_generator,


@app.cell
def __():
    #survey_generator(behavioral_questions)
    return


@app.cell
def __():
    ### third page: personality calculations
    return


@app.cell
def __(graphs, mo, sentence_results, submit_survey):
    mo.vstack(
        [sentence_results,
        graphs]
    ) if (submit_survey.value) else None
    return


@app.cell
def __(behavioral_answers_int, expert_weights, mo, util):
    breakdown_normal = util.breakdown(behavioral_answers_int)
    breakdown_validated = util.breakdown_weighted(behavioral_answers_int, expert_weights)
    graphs = mo.ui.tabs(
        {
            "**Pure Personality**": util.plot(breakdown_normal),
            "**Personality with Validator Weights**": util.plot(breakdown_validated),
        }
    ).center()
    return breakdown_normal, breakdown_validated, graphs


@app.cell
def __():
    return


@app.cell
def __():
    ### database management
    return


@app.cell
def __():
    # cols = 0
    # if len(participant_obs) == cols:
        # submit row to backend database
        # print
    return


if __name__ == "__main__":
    app.run()
