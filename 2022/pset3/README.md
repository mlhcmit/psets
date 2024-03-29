# Problem Set 3


**This problem set is due Wednesday, March 9th, at 11:59 p.m. Please submit your write-up or Colab notebook in PDF format to Gradescope. If you are submitting a separate write-up, please make sure you include coding tasks in your write-up. Your submission should be name as ${mit_email_username}.pdf (e.g. wboag.pdf). You must write up your problem sets individually. You should not share your code or solutions (i.e., the write-up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior cannot be tolerated in any academic environment that prides itself on individual accomplishment. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.**

(IMPORTANT) If you are submitting a pdf version of your notebook, please **remove cells and outputs (e.g. boilerplate/provided codes, instructions, model training logs, and etc.) that are not directly relevant to the write-up questions.**

## Problem 1: Interpretability for Chest X-Ray Diagnosis Models
### Overview

In this problem, we will work with a subset of the MIMIC-CXR dataset, distributed through PhysioNet as in
previous PSets. We will present you with a simulated experience of evaluating a potential model for deployment. In
this case, the model in question (which we will provide to you, fully trained) is being evaluated for its use
in the detection of [Pneumothorax (PTX)](https://en.wikipedia.org/wiki/Pneumothorax); a potentially dangerous
condition often colloquially known as a collapsed lung. Ultimately, your desired use case for this model is to
use it as a diagnostic aid for new patients to the ED.



However, being an experienced MLHC researcher, you're concerned that perhaps this model is not actually
leveraging viable diagnostic information to make its PTX decision--instead, it may be confounded by other
factors in the data. You'll leverage 4 interpretability techniques to assess this risk:
  1. Error Auditing, in which you'll examine different kinds of errors the model makes,
  2. Interpretability Visualizations, in which you'll implement two algorithms for visualizing the salient
     regions of the image for a CNN model, then use those to examine a subset of the images.
  3. Multimodal Analysis, in which you'll use the associated free-text reports to do a targeted investigation
     of image confounders, and,
  4. Error Stratification, in which you'll implement a (very simple) classifier over the reports in order to
     split images according to our confounder of concern, then examine the model's performance when the
     confounder is absent.

Ultimately, in each of these sections you'll be asked to comment on any strategies you see, and, at the end,
answer several concluding questions.

### Learning Goals
Interpretability is often touted as being critical in machine learning for healthcare for its use in improving
the trust of downstream end-users in the model; however, this overshadows what may be an even more important
role of interpretability / explainability in ML4H -- namely, its use for creators of models to gain confidence
in their model's internal and external validity. Here, we task you with using interpretability methods for
exactly this purpose, in a real-world setting of examining whether or not a trained model that performs well
according to traditional metrics is really ready for deployment. In addition, other learning goals include:
  * To think through possible confounders of a model designed for clinical use.
  * To gain familiarity with two basic forms of CNN visualization.
  * To demonstrate the power of leverarging multimodal information for interpretability.
  * To question the accuracy of automatic labels / gain exposure to label noise
  * To gain an introduction to CNNs/CV/radiograph data.

### Code and Write-up Questions
Code and write-up questions can be found [here](https://colab.research.google.com/drive/1pQjhmPh5a4zgKnpP7EFyyzLJVhrrQVJW?usp=sharing). (IMPORTANT) Please save the notebook into your drive (File -> Save a copy in Drive) then start working on it.
