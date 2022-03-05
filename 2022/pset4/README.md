# Problem Set 4

**This problem set is due Wednesday, March 18th, at 11:59 p.m. Please submit your write-up or Colab notebook in PDF format to Gradescope. If you are submitting a separate write-up, please make sure you include coding tasks in your write-up. Your submission should be name as ${mit_email_username}.pdf (e.g. wboag.pdf). You must write up your problem sets individually. You should not share your code or solutions (i.e., the write-up) with anyone inside or outside of the class, nor should it be posted publicly to GitHub or any other website. You are asked on problem sets to identify your collaborators. If you did not discuss the problem set with anyone, you should write "Collaborators: none." If in writing up your solution you make use of any external reference (e.g. a paper, Wikipedia, a website), both acknowledge your source and write up the solution in your own words. It is a violation of this policy to submit a problem solution that you cannot orally explain to a member of the course staff. Plagiarism and other dishonest behavior cannot be tolerated in any academic environment that prides itself on individual accomplishment. If you have any questions about the collaboration policy, or if you feel that you may have violated the policy, please talk to one of the course staff.**

(IMPORTANT) If you are submitting a pdf version of your notebook, please **remove cells and outputs (e.g. boilerplate/provided codes, instructions, model training logs, and etc.) that are not directly relevant to the write-up questions.**

## Part I :




## Part II : Implementing propensity scores re-weighting and covariate adjustment methods in Python

Now that you have gained conceptual and theoretical understanding of causal inference analysis in Part I, for this part, you will get a chance to apply your understanding to analyzing real-world dataset and building a pipeline in Python. Your main task is to estimate the average treatment effect (ATE) of quitting smoking T on weight gain Y, using the [NHEFS](https://wwwn.cdc.gov/nchs/nhanes/nhefs/default.aspx/) dataset. 

Your main learning objectives include :
1. Understand a mechanism of how confounders, when unadjusted, can introduce bias into the ATE. 
2. Learn how to implement propensity scores re-weighting to obtain the ATE in Python.
3. Learn how to implement covariate adjustment strategies to obtain the conditional average treatment effect (CATE) as well as ATE in Python.
4. Assess how robust estimated ATE is against potential unobserved confounders via sensitivity analysis. 

### Code and Write-up Questions
Code and write-up questions can be found [here](https://colab.research.google.com/drive/1StClzgknVBwCBp_kPue7W1Km4nwWs3uv?usp=sharing). (IMPORTANT) Please save the notebook into your drive (File -> Save a copy in Drive) then start working on it.

References :
[1] : Hernán MA, Robins JM (2020). Causal Inference: What If. Boca Raton: Chapman & Hall/CRC

[2] : Neal (2020). Introduction to Causal Inference from a Machine Learning Perspective
