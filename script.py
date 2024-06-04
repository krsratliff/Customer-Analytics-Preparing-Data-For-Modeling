########
# IMPORT
########

# libraries
import pandas as pd
import numpy as np

# dataframe to start with, copy to transform
ds_jobs = pd.read_csv('customer_train.csv')
ds_jobs_transformed = ds_jobs.copy()

# file to print information to
filename = 'info.md'
f = open(filename, 'w')






#################
# BOOLEAN COLUMNS
#################

print(
    '# BOOLEAN COLUMNS',
    file = f
)

# Find boolean columns
#   Result: relevant_experience, job_change

print(
    '## Columns with two unique values',
    file = f
)

print(
    ds_jobs.nunique()[
        ds_jobs.nunique() == 2
    ],
    file = f
)

# find unique values of boolean columns
print(
    '\n### relevant_experience unique values',
    file = f
)

print(
    ds_jobs['relevant_experience'].value_counts(),
    file = f
)

print(
    '\n### job_change unique values',
    file = f
)

print(
    ds_jobs['job_change'].value_counts(),
    file = f
)

# true values for boolean columns
relevant_experience_true = 'Has relevant experience'
job_change_true = 1.0

# dict: column name -> true value of column
bool_col_true_val = {
    'relevant_experience' : relevant_experience_true,
    'job_change' : job_change_true
}

# make boolean column in transformed df
for col in bool_col_true_val.keys():
    ds_jobs_transformed[col] = np.where(
        ds_jobs[col] == bool_col_true_val[col], # if value is bool_col_true_val[col]...
        True, False # ... yield True; otherwise yield False
    )

# verify dtypes

print(
    '## Verifying boolean dtypes',
    file = f
)

print(
    ds_jobs_transformed[
        [col for col in bool_col_true_val.keys()]
    ].dtypes,
    file = f
)





#######################
# INT AND FLOAT COLUMNS
#######################

print(
    '# INT AND FLOAT COLUMNS',
    file = f
)

# print dtypes to find int and float columns

current_dtypes = ds_jobs_transformed.dtypes.apply(str) # current dtypes as strings

current_dtypes[
    ~current_dtypes.isin(['bool', 'object'])
    ]

print(
    '## Non-bool, non-object columns',
    file = f
)

print(
    current_dtypes[
        ~current_dtypes.isin(['bool', 'object'])
    ],
    file = f
)


# result: 
#   student_id and training_hours are int, 
#   city_development_index is float


# transforming
int_col = ['student_id', 'training_hours']
float_col = ['city_development_index']

for col in int_col:
    ds_jobs_transformed[col] = ds_jobs[col].astype('int32')

for col in float_col:
    ds_jobs_transformed[col] = ds_jobs[col].astype('float16')



# verifying
print(
    '## Verifying int and float conversion',
    file = f
)

print(
    ds_jobs_transformed[
        int_col + float_col
    ].dtypes,
    file = f
)









#####################
# CATEGORICAL COLUMNS
#####################

print(
    '# CATEGORICAL COLUMNS',
    file = f
)

# find object columns
current_dtypes = ds_jobs_transformed.dtypes.apply(str)

print(
    '## Columns with object dtype',
    file = f
)

print(
    current_dtypes[current_dtypes.isin(['object'])],
    file = f
)

# results
#   nominal categories
nom_cat = [
    'city', 
    'gender', 
    'major_discipline', 
    'company_type'
    ]

#   ordinal categories
ord_cat = [
    'enrolled_university', 
    'education_level', 
    'experience', 
    'company_size', 
    'last_new_job'
    ]

# convert categories to category dtype
for col in nom_cat + ord_cat:
    ds_jobs_transformed[col] = ds_jobs[col].astype('category')


# verify complete conversion
print(
    '## Verifying column dtypes',
    file = f
)

print(
    ds_jobs_transformed.dtypes,
    file = f
)



# find values of ordinal categories
print(
    '## Values of ordinal categories',
    file = f
)

for col in ord_cat:
    print('### ' + col, file = f)
    print(
        ds_jobs[col].value_counts(),
        file = f
    )


# results in order
ord_cat_vals = {}

#   enrolled_university values
ord_cat_vals['enrolled_university'] = [
    'no_enrollment',
    'Part time course',
    'Full time course'
]

#   education_level values
ord_cat_vals['education_level'] = [
    'Primary School',
    'High School',
    'Graduate',
    'Masters',
    'Phd'
]

# experience values
ord_cat_vals['experience'] = ['<1'] +\
    [str(n) for n in range(1,21)] +\
    ['>20']

# company_size values
ord_cat_vals['company_size'] = [
    '<10',
    '10-49',
    '50-99',
    '100-499',
    '500-999',
    '1000-4999',
    '5000-9999',
    '10000+'
]

# last_new_job values
ord_cat_vals['last_new_job'] = ['never'] +\
    [str(n) for n in range(1,5)] +\
    ['>4']


# check that ord_cat and ord_cat_vals.keys() line up

print(
    '## Verifying ordering dictionary keys',
    file = f
)

print(
    'Ordering dictionary matches list of ordered columns: ' +\
    str(list(ord_cat_vals.keys()) == ord_cat),
    file = f
)


# apply ordering
for col in ord_cat_vals.keys():
    ds_jobs_transformed[col] =\
        ds_jobs_transformed[col].cat.reorder_categories(
            new_categories = ord_cat_vals[col],
            ordered=True
        )

# verify ordering
print(
    '## Verifying ordering',
    file = f
)

for col in ord_cat_vals.keys():
    print('### ' + col, file = f)
    print(
        ds_jobs_transformed[col].unique().sort_values(),
        file = f
    )


# memory usage pre-filter
#   function to reuse later
def CheckMemorySavings(df_old, df_new, f):
    # calculate
    old_usage = df_old.memory_usage().sum()
    new_usage = df_new.memory_usage().sum()
    percent_reduced = round(
        100*(old_usage - new_usage) / old_usage,
        1
    )

    # print
    print(
        'Original memory usage: ' + str(old_usage),
        file = f
    )

    print(
        'New memory usage: ' + str(new_usage),
        file = f
    )

    print(
        'Percent reduced: ' + str(percent_reduced) + '%',
        file = f
    )


# check memory usage after filtering
print(
    '# Memory usage before filtering',
    file = f
)

CheckMemorySavings(ds_jobs, ds_jobs_transformed, f)







###########
# FILTERING
###########

# want students with only 10 or more years of experience
#   and at companies w/ at least 1000 employees

ds_jobs_transformed = ds_jobs_transformed[
    (ds_jobs_transformed['experience'] >= '10')
    &
    (ds_jobs_transformed['company_size'] >= '1000-4999')
].copy()

# verifying filter

print('# FILTERING', file = f)

print('New minima for filtered columns: ', file = f)

print(
    'Experience: ' + str(ds_jobs_transformed['experience'].min()),
    file = f
)

print(
    'Company size: ' + str(ds_jobs_transformed['company_size'].min()),
    file = f
)


###########
# FINISHING
###########


# check memory usage after filtering
print(
    '# Memory usage after filtering',
    file = f
)

CheckMemorySavings(ds_jobs, ds_jobs_transformed, f)



# export transformed dataset
ds_jobs_transformed.to_csv('customer_train_transformed.csv')

# close file
f.close()