# Problem set 1

**This problem set is due Wed. Feb 16 at 11:59pm EST. Please submit your write-up and code. When you write up your report, put all writing into one file and name it ${mit_email_username}.pdf (e.g. itmoon.pdf). You must write up their problem sets individually. You should not share your code or solutions (i.e., the write up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior cannot be tolerated in any academic environment that prides itself on individual accomplishment. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.**


We are interested in predicting hospital mortality from clinical records.

By now, you should have access to the [MIMIC-III](https://mimic.physionet.org/gettingstarted/access/) dataset. If you do not, please refer to Problem Set 0. If you still have problems with access to the data, please contact the course staff through Piazza. 

The MIMIC-III database is 40-50 GB, so although all data comes from MIMIC-III, we have parsed it for your convenience. We will be using Google Colab for this Pset (essentially an IPython notebook in the cloud), since Physionet has made it possible to query MIMIC via Google Cloud. We will provide View-only versions of the Colab notebook, and you can make a copy for your own work. Note that when you run these notebooks, you may see a warning that states that the notebook was not authored by Google but instead by 7itmoon@gmail.com-- this is expected and not a problem. Simply click "Run Anyway" and proceed.

## 0: Accessing Google Cloud Platform [0 points]

The MIMIC database is 40-50 GB. Given its large size, instead of your working with it locally, we will be creating subsets of data for you to work with, which you can access via Google Cloud. 

Please follow the following steps to get your Google account connected with MIMIC:

 - (Optional) Create a free Google Cloud Platform (GCP) account connected to a Gmail; you may need the GCP for a class project and upcoming psets when utilizing addtional computing resources (e.g. GPU)
 - Link the Gmail to your Physionet account. See detailed instructions on how to do so [here](https://mimic.physionet.org/gettingstarted/cloud). 
 - Request access to MIMIC on GCP: Go the PhysioNet MIMIC-III page, [Files section](https://physionet.org/content/mimiciii/1.4/#files), and click "Request access" to the files using Google Cloud Storage Browser. If you have previously signed up for MIMIC-IV, not MIMIC-III, you may need to additionally sign the data user agreement (DUA) for MIMIC-III, and the approval should be processed immediately. (IMPORTANT) Make sure you click on "Request access", not "Google Cloud Storage Browser" and confirm that you see "Access to the GCP bucket was granted to your_ID@gmail.com for project: MIMIC-III Clinical Database v1.4" on the top of the screen.
 - Check whether you can run the steps in the following [Colab notebook](https://colab.research.google.com/drive/1xReyOAF-dBivEHKJk88HPd9GMZaftxm8?usp=sharing). You may need to make a copy of it to run it.

## 1: Data exploration [10 points]
The first step when accessing a new dataset is to explore the dataset and try to marry your understanding of the data generative process (in this case, clinical care) with the reality of the data you observe. Misunderstandings about the nature of the data can hamper effective modelling, or make models look much more effective than they really would be in deployment. In this part, we will explore the _unstructured_ data in MIMIC---in particular, the clinical notes. In later parts, we'll explore other aspects of the data. We hope that you find this exercise useful in understanding the clinical care received by patients. When everything is just dataframes and vectors, it might be easy to lose sight of the fact that we are trying to use data to help real people with serious problems.

In the notebook [chart_review.ipynb](https://colab.research.google.com/drive/1hZFU-RaWjzRFEiKCrogPvEaPzU56tksQ?usp=sharing), we will first walk through one patient's hospital stay together in the section "Patient 1". Then, in the section "Patient 2", you will be asked to mirror that exploration on a new patient, and answer the following questions for your PSet write-up (these will make more sense based on the content in the earlier parts of the notebook):

1.1) What is the patient's History of Present Illness?

1.2) How long were they in the hospital?

1.3) What are three of the major events in the timeline of this patient's care?

1.4) What stood out to you most when reading the nursing notes?


## 2. Structured data (logistic regression) [10 pooints]

For sections 2-4, you can create a copy of [this Colab notebook](https://colab.research.google.com/drive/1Iq9tiF_JQZFkbI4jJhgauAdCTSaJbfC7?usp=sharing), which contains links to the data files you need. 

We have provided the first-collected lab results from the first 48 hours of a patient’s stay. Take a look through the data of `adult_icu.gz`, saved in the colab to `lab_df` and the associated code that generated it in `mort_hosp_cleanup.py`. 

2.1) What do the columns seem to mean? If we wanted to predict in-hospital mortality, which column would we use as the outcome column? Which columns would be features and which columns would NOT be features?

Using [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), train a logistic regression classifier on the training data while optimizing for best train accuracy, find the best hyperparameters among `C=[0.1,0.25,0.5,1.]` and `penalty=[‘l1’,’l2’]` on validation data. Normalize your feature values to have zero mean and unit variance.

2.2) What is the accuracy on test data? What is the AUC? Create a confusion matrix of your predictions against reality. Look at the proportion of patients who died in the hospital, and explain why might one metric be more informative than the other.

2.3) What are the most predictive features, based on the the coefficients of the logistic regression? Comment on your findings.

## 3. Clinical notes (logistic regression) [10 points]

Clinical notes can be a rich source of unstructured information. For ease of computation, we randomly selected 15,000 patients from the dataset and supplied the notes from the first 48 hours in `adult_notes.gz`. these have been loaded in the colab into the dataframe `note_df`.

Use a count vector of a bag of words of the 5000 most popular words (i.e. the 5000 words with the highest term frequency) and a logistic regression trained to optimize the data accuracy. Note that this prediction task is only using the clinical notes and not using any structured data from the previous section. We suggest using [sklearn Count Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) here for your feature generation.

Train on training data and find the best hyperparameters among `C=[0.1,0.25,0.5,1.]` and `penalty=[‘l1’,’l2’]` on validation data. 

3.1) What is the accuracy and AUC on the test data? How do these results compare to structured data results?

3.2) What words are the most predictive (positive and negative) of hospital mortality? Look up any unknown clinical definitions and comment on a few. 

## 4 Analysis [10 points]

It is important to understand who makes up your dataset and how your model performs on different subpopulations. We will do this on the lab dataset from question 2. 

4.1) For each of the 5 ethnic categorizations provided in `adult_icu.gz`, how many people belong to each group? Are the hospital mortality rates the same for each group? 

4.2) Create a histogram of the ages in the dataset (in buckets of 10: 20-29, 30-39, etc), and another bar plot of mortality rates of each bucket. What bucket has the highest mortality? The lowest?

4.3) So that your answer doesn't depend on whether you found the best model in #2, retrain a model on the training set using C=1 and penalty='l2'. Evaluate your new model (AUC, accuracy) on patients in the test set who are less than 40, and patients in the test set who are older than 40. For what group is performance better? Can you hypothesize why? 
