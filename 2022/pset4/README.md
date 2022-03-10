# Problem Set 4

This problem set is due Friday, March 18th, at 11:59 p.m. Please submit your write-up in PDF format to Gradescope. You may write up Part 1 separately and then merge the pdf with the Colab notebook pdf or you may have a single write-up where you include the coding tasks where required. Your submission should be named as ${mit_email_username}.pdf (e.g. wboag.pdf). You must write up your problem sets individually. You should not share your code or solutions (i.e., the write-up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior will not be tolerated. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.

(IMPORTANT) If you are submitting a pdf version of your notebook, please **remove cells and outputs (e.g. boilerplate/provided code, instructions, model training logs, etc.) that are not directly relevant to the write-up questions.**

## Part I : Implications of Lack of Overlap in Causal Inference
We will begin with a deep dive into a core assumption in causal inference: overlap (also known as common support or positivity). See this document for the first part of the problem set: [Part 1](./ps4-part1-final.pdf).

Your main learning objectives include: 
1. Understand how one's estimate of the ATE changes in regions of overlap when different parametric assumptions are made.
2. Reason about the identifiability of the ATE in covariate regions with no overlap.
3. Understand conceptually how to reason about the output of the IPW estimator when there is a lack of overlap. 

## Part II : Implementing propensity scores re-weighting and covariate adjustment methods in Python

In Part II of the Problem Set, you will get a chance to apply your understanding of causal analysis on a real-world dataset. Your main task is to estimate the average treatment effect (ATE) of quitting smoking (T) on weight gain (Y), using the [NHEFS](https://wwwn.cdc.gov/nchs/nhanes/nhefs/default.aspx/) dataset. 

Your main learning objectives include:
1. Understand a mechanism of how confounders, when unadjusted, can introduce bias into the ATE estimate. 
2. Learn how to implement propensity score re-weighting to estimate the ATE in Python.
3. Learn how to implement covariate adjustment strategies to estimate the conditional average treatment effect (CATE) as well as ATE in Python.
4. Assess how robust the estimated ATE is against potential unobserved confounders via sensitivity analysis. 

### Code and Write-up Questions
Code and write-up questions can be found [here](https://colab.research.google.com/drive/1StClzgknVBwCBp_kPue7W1Km4nwWs3uv?usp=sharing). (IMPORTANT) Please save the notebook into your drive (File -> Save a copy in Drive) before starting to work on it.

References :

[1] : Hernán MA, Robins JM (2020). Causal Inference: What If. Boca Raton: Chapman & Hall/CRC

[2] : Neal (2020). Introduction to Causal Inference from a Machine Learning Perspective

[3] : Gelman, A., & Hill, J. (2006). Data Analysis Using Regression and Multilevel/Hierarchical Models (Analytical Methods for Social Research). Cambridge: Cambridge University Press.
