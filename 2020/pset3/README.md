# Problem Set 3

**This problem set is due Friday, April 3rd, at 5:59 p.m. Please submit your code and write-up. You must
submit two separate files; one pdf containing ALL your written solutions (including any notebook output that
is relevant to contextualize your answer) to Gradescope, and one ipython notebook containing your code to Stellar. Your work must stand
alone, be clear, concise, and generally well written, and not only provide answers to explicit questions we
ask, but more generally demonstrate your thought process and understanding of the material in question. Please
note any and all collaborators, as well as slack days used. You may not share your code, our starter code or
data files, or your write-up with anyone.**

## Problem 1: Interpretability for Chest X-Ray Diagnosis Models
### Overview

In this problem, we will work with a subset of the MIMIC-CXR dataset, distributed through PhysioNet as in
PSet 1. We will present you with a simulated experience of evaluating a potential model for deployment. In
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

### Link
Problem 1 can be found here: https://colab.research.google.com/drive/1FptyMr6_UQoe4Estox3M1ltP-oQY971F

You will be required to turn in both your final `.ipynb` colab file and include in your single separate writeup
the answers to all questions explicitly asked in the "Write-Up Questions" sections.

## Problem 2: Learning to Defer
### Overview

Clinicians and algorithms have different strengths, and as a result, a combination of the two can be more
potent than either alone. In this problem, you will gain practice thinking about the tradeoffs involved when
you have both human and algorithmic decision-makers in play. Specifically, you will work through optimization
problems as they relate to the "Learning to Reject" and "Learning to Defer" paradigms, as well as variations
of those paradigms. 

### Learning Goals
There is no one correct answer as to the best way to allocate clinician resources vs. algorithmic power. As a
result, any optimization problem inherently depends on the context of the clinical problem and what decision
makers choose to value. Therefore, it is valuable for you to feel comfortable setting up optimization problems
in different contexts, so that in the future, you are able to adapt to a new context with different
constraints. 

### Link
Problem 2 can be found here: https://drive.google.com/file/d/1FvtJgH8wydhyi8hczb0x3pFc2diHayb5/view?usp=sharing

## Problem 3: Dataset Shift
### Overview
In machine learning, we often learn models under the assumption that examples at training time and examples at
prediction time are pulled from the same distribution. In medical settings, this assumption is often untrue.
Within a given hospital, there are constant changes in medical practice and medical documentation (e.g. ICD9
vs ICD 10, Careview vs Metavision), and that's not even to mention the differences between hospitals.
Therefore, here you will work through understanding the different ways your data can shift and how to
formulate that shift mathematically. 

### Learning Goals
The goal is to be able to recognize instances where dataset shift may occur in clinical contexts and
understand how to characterize that distributional shift mathematically, since that is the first step in
understanding whether it is possible to mitigate the downstream effects and if so, how. 

### Link
Problem 3 can be found here: https://drive.google.com/open?id=1dbuFJr_10fD8hU2UEOnFoNBDC2PBVvBl

## Problem 4: Logistics
**Responses to this question are greatly appreciated but not graded in any way shape or form.**
Once you've completed this problem set, please fill out this form: https://forms.gle/hBfc2ccBW7sy5vASA and let
us know how long it took you, how easy you found it to understand and/or complete, and any other feedback you
have. Thank you!
