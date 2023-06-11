import pandas as pd
import numpy as np

# issues file
df_issues = pd.read_excel('/Users/vedantchauhan/PycharmProjects/pythonProject/data_exploration_all.xlsx')
print(df_issues)
# issues output classified file
df_issues_output = pd.read_excel('/Users/vedantchauhan/Downloads/dataset-output.xlsx')
print(df_issues_output)

'''for name, values in df_issues.iteritems():
    print(name)
    print(values)'''

for i in df_issues['issue_body']:
    for o in df_issues_output['Issue body']:
        if str(o) in str(i):
            print(o)

'''rows_list = []
count = 0
for i_index, i_values in df_issues.iterrows():
    for o_index, o_values in df_issues_output.iterrows():
        git_project = i_values[0]
        issues_body = i_values[1]
        output_issues_body = o_values[0]
        output_classification = o_values[1]
        output_hcd = o_values[2]
        output_non_hcd = o_values[3]
        output_category = o_values[4]
        if str(output_issues_body) in str(issues_body):
            dict = {'git_project' : git_project,
                    'issue_body' : output_issues_body,
                    'AppUsage, Inclusiveness, User reaction, Non-human-centric' : output_classification,
                    'Human-centric' : output_hcd,
                    'Non-human centric' : output_non_hcd,
                    'Category' : output_category
                    }

            rows_list.append(dict)

df = pd.DataFrame(rows_list)
print(df)'''
#df.to_excel("data_combine.xlsx", index=False)
# take all columns from output and add git_project column from issues