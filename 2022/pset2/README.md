# Problem Set 2


**This problem set is due Wednesday, Feb 25th, at 11:59 pm EST. Please submit your write-up in PDF format to Gradescope. When you write up your report, put all writing into one file and name it ${mit_email_username}.pdf (e.g. wboag.pdf). Note that you may submit a PDF version of your notebook only if you can clearly indicate answer for each problem and comment your code such that graders can easily follow your work. You must write up your problem sets individually. You should not share your code or solutions (i.e., the write-up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior cannot be tolerated in any academic environment that prides itself on individual accomplishment. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.**

## Before you begin the problem set...
In this problem set, you'll work with a real-world healthcare dataset (2014 De-identification and Heart Disease Risk Factors Challenge) collected as a part of n2c2 NLP Research initiative. To do that, you'd need to sign the corresponding DUA. Please see insturctuions [here](https://canvas.mit.edu/courses/13812/discussion_topics/140997). We'd recommend completing the DUA process as early as you can. 

## Problem 1: Clinical Concept Extraction
### Overview
In this problem, we explore the use of annotation of clinical text with _clinical concepts_ through the tool MetaMap. We will provide you a set of concepts extracted from MetaMap, and you will look through them, clean these extracted concept instances by identifying concepts that are especially prone to misclassification, and then finally use these extracted concepts to build a disease-symptom cooccurrence matrix, which can be used to quantify significant associations between the two.

### Learning Goals
Clinical concepts are an extremely commonly used tool. They allow us to translate unstructured text into structured data, with extracted entities often related to one-another through rich relationships encoded in external knowledge graphs describing these clinical concepts. Even in the simple context of mining a set of unstructured notes to determine common comorbidities in a population, the goal presented here, clinical concepts enable far more insightful data exploration and comorbidity discovery than would be possible working with raw text alone. In this problem, we hope you
  1. Gain an appreciation for working with common clinical extraction toolkits---in particular, MetaMap
  2. Understand the failure points of concept extraction tools and the challenges of the extraction task 
  3. Understand how we can use concept extraction to quickly mine well understood structured data from a large collection of unstructured clinical notes, and
  4. How we can use those concepts for downstream analyses

### Code & Materials
You will use the notebook linked [here](https://colab.research.google.com/drive/1mYKk_STC9-2TmkPNqXaIvFAkvUCive4Q?usp=sharing).
(IMPORTANT) Please save the notebook into your drive (File -> Save a copy in Drive) then start working on it.

The notebook contains detailed instructions and includes 8 short questions (1.1 through 1.8). In the final write-up PDF, please also include all the codes you've added/changed for answering the questions in a different color and font family. No need to upload the colab notebook.


## Problem 2: Clinical Natural Language Processing (NLP) for De-identification
### Overview
In this problem, we explore the use of different modeling techniques for working with clinical text on a common, foundational task in many data-acquisition pipelines in machine learning for healthcare: de-identification. Using the [N2C2](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/#) 2014 de-identification dataset, we will explore baseline and recurrent neural network models for automatically identifying personal health information (PHI) elements from within the text. If trained properly, such a model could be used to pre-screen clinical text prior to release to catch and flag any remaining instances of PHI in the text (which would then be obfuscated prior to release).

**IMPORTANT**: In order to access the data, you *MUST* register, login and sign DUA via [N2C2 NLP Research Data Sets portal](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/) before starting the Pset.

### Learning Goals
Clinical NLP is one of the primary areas where many practical deployment areas do exist already (de-identification pipelines are used routinely by data providers in this field), even though many of these practical opportunities for use are more operational, logistical, or research-backing rather than clinical. It is also easy to think, given the many successes we've seen in general NLP with advanced neural network models, that baselines are only likely to be of limited success.

In this problem, we hope to show you
  1. What it is like to work with clinical text in a modern NLP pipeline, end to end,
  2. Think critically about how to iteratively craft a strong baseline for this real-world clinical text task and to understand what kinds of changes most impact baseline performance.
  3. Examine the performance differences between an advanced neural network model and your own focused baseline, and
  4. Comment on these differences, attempting to generalize to broader factors that may indicate when neural models would be more or less appropriate than simpler baselines (though such conjectures would, by their nature, by speculative).
  5. Understand the different kinds of de-identification one might perform.

### Code & Materials
You can find the colab notebook for this problem [here](https://colab.research.google.com/drive/1Nb0yGOUKMmFakIUkTRFTWYn3n-PHnOJv?usp=sharing). Please save the notebook into your drive (File -> Save a copy in Drive) then start working on it.

This notebook contains detailed instructions for this problem, including walking you through some pre-done dataset analysis and baseline models prior to diving into your specific deliverables. For reference, we ask you to answer a number of questions about baselines/data exploration and the neural network model. 

In the final write-up PDF, please also include all the codes you've added for answering the questions in a different color and font family, and be sure the code parts are equally easy to follow and subdivide.

**Note:** This notebook contains _a lot_ of boilerplate code that we've worked through for you, along with a lot of text and other information. At the same time, we ask relatively few questions and have you actually implement relatively little. _However_, that "relatively little" can turn into quite a lot if you do not take the time to read the notebook thoroughly and understand the code prior to diving into the final deliverables, so we strongly encourage you to read the code end to end before beginning any of the specific questions.
