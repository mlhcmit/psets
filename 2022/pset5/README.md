# Problem Set 5

This problem set is due Wednesday, April 20th, at 11:59 p.m. Please submit your write-up in PDF format to Gradescope. You may write up Part 1 separately and then merge the pdf with the Colab notebook pdf or you may have a single write-up where you include the coding tasks where required. Your submission should be named as ${mit_email_username}.pdf (e.g. wboag.pdf). You must write up your problem sets individually. You should not share your code or solutions (i.e., the write-up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior will not be tolerated. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.

(IMPORTANT) If you are submitting a pdf version of your notebook, please **remove cells and outputs (e.g. boilerplate/provided code, instructions, model training logs, etc.) that are not directly relevant to the write-up questions.**

## Part I : Learning from Noisy Labels
### Overview
In this problem, you will build on the proofs for learning from noisy labels we worked through during class. Specifically, you will be investigating the anchor-and-learn approach as well as how to leverage noisy labels at prediction time, if they're available. See this document for the first part of the problem set: [Part 1](./6_871_ps5_tex_2022.pdf).

### Learning Goals
Medical data is messy and true gold labels are often hard or prohibitively expensive to obtain in bulk. As a result, it is often necessary to leverage noisy labels in the training process. 
In this problem, we hope you:
1) Solidify your understanding of how training from noisy labels works,
2) Recognize scenarios in which noisy labels may be available at prediction time,
3) And understand both theoretically and intuitively why noisy labels at prediction time can lead to more accurate performance.

## Part II : Survival Analysis
### Overview
In this part of the problem set, we'll walk you through data pre-processing, survival model development, and model evaluation for widely-used semi-parametric and parametric survival models. At the end, you will build a deep-learning based survival model and compare its performance to the performance of conventional baseline models.
 
### Learning Goals
1. Understand modeling assumptions for different types of survival models.
2. Learn how to create a Python pipeline for survival model development and evaluation.
3. Learn how a deep-learning based approach can be applied to survival modeling.

### Code and Write-up Questions
Code and write-up questions can be found [here](https://colab.research.google.com/drive/1Oc2yRdOqv4BVVMGLXBZ1c0Mdeeio-V-w?usp=sharing). (IMPORTANT) Please save the notebook into your drive (File -> Save a copy in Drive) before starting to work on it.

### Pset feedback :
Once you complete the problem set, please complete [the feedback form](https://forms.gle/vriE3aPxvDvJoc2f7). We're eager to hear your thoughts/feedback on the pset! 
