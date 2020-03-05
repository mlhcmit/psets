# Problem Set 2


**This problem set is due Wednesday, March 4th, at 11:59 p.m. Please submit your code to Stellar and your write-up to Gradescope. All students who submitted PSET 1 were added to the course's Gradescope roster, and you should have received an email (to your MIT email) to that effect. If you feel there's been an error, let us know and we can manually add you. You must submit two separate files; one pdf containing your written solutions (to Gradescope), and a zip of ipython notebooks containing your code (to Stellar). Your work must stand alone, be clear, concise, and generally well written, and not only provide answers to explicit questions we ask, but more generally demonstrate your thought process and understanding of the material in question. Please note any and all collaborators, as well as slack days used on the top of your PDF write-up. You may not share your code, our starter code or data files, or your write-up with anyone.**

## Problem 1: Clinical Concept Extraction
### Overview
In this problem, we explore the use of annotation of clinical text with _clinical concepts_ through
the tool MetaMap. We will provide you a set of concepts extracted from MetaMap, and you will look through them, clean
these extracted concept instances by identifying concepts that are especially prone to misclassificaiton, and then
finally use these extracted concepts to build a disease-symptom coccurence matrix, which can be used to
quantify significant associations between the two.

### Learning Goals
Clinical concepts are an extremely commonly used tool. They allow us to translate unstructured text into
structured data, with extracted entities often related to one-another through rich relationships encoded in
external knowledge graphs describing these clinical concepts. Even in the simple context of mining a set of
unstructured notes to determine common comorbidities in a population, the goal presented here, clinical
concepts enable far more insightful data exploration and comorbodity discovery than would be possible working
with raw text alone. In this problem, we hope you
  1. Gain an appreciation for working with common clinical extraction toolkits---in particular, MetaMap
  2. Understand the failure points of concept extraction tools and the challenges of the extraction task 
  3. Understand how we can use concept extraction to quickly mine well understood structured data from a large
     collection of unstructured clinical notes, and
  4. How we can use those concepts for downstream analyses

### Code & Materials
You will use the notebook linked here: https://colab.research.google.com/drive/1Jxj3hQ5pSST0KmnFG2TKUslG-00eFMWc.

The notebook contains detailed instructions and includes 8 short questions (1.1 through 1.8). Please include your answers to these questions in the separate PDF write-up.

## Problem 2: Clinical Natural Language Processing (NLP) for De-identification.
### Overview
In this problem, we explore the use of different modeling techniques for working with clinical text on a
common, foundational task in many data-acquisition pipelins in machine learning for healthcare:
de-identification. Using the [N2C2](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/#) 2014
de-identification dataset, we will explore baseline and recurrent neural network models for automatically
identifying personal health information (PHI) elements from within the text. If trained properly, such a model
could be used to pre-screen clinical text prior to release to catch and flag any remaining instances of PHI in
the text (which would then be obfuscated prior to release).

**IMPORTANT**: In order to access the data (we will email you the files you need to run the colab), you *must*
fill out this data use agreement (DUA) form. It takes no more than 10 minutes. Form:
https://forms.gle/WBCyqqwuC7nxvt838

### Learning Goals
Clinical NLP is one of the primary areas where many practical deployment areas do exist already
(de-identification pipelines are used routinely by data providers in this field), even though many of these
practical opportunities for use are more operational, logistical, or research-backing rather than clinical. It
is also easy to think, given the many successes we've seen in general NLP with advanced neural network models,
that baselines are only likely to be of limited success.

In this problem, we hope to show you
  1. What it is like to work with clinical text in a modern NLP pipeline, end to end,
  2. Think critically about how to iteratively craft a strong baseline for this real-world clinical text task
     and to understand what kinds of changes most impact baseline performance.
  3. Examine the performance differences between an advanced neural network model and your own focused
     baseline, and
  4. Comment on these differences, attempting to generalize to broader factors that may indicate when neural
     models would be more or less appropriate than simpler baselines (though such conjectures would, by their
     nature, by speculative).
  5. Understand the different kinds of de-identification one might perform.

### Code & Materials
You can find the colab notebook for this problem here:
https://colab.research.google.com/drive/1fpXtH5yaTTNHKImU_4MrJtYJ_QM3l8qP

This notebook contains detailed instructions for this problem, including walking you through some pre-done
dataset analysis and baseline models prior to diving into your specific deliverables. For reference, we ask
you to answer a number of questions about baselines/data exploration and the neural network model.  In your
final write-up, please indicate carefully which question you are answering where, and be sure your code is
equally easy to follow and subdivide. Use text cells in colab liberally to add higher level structure to your
notebook.

**Note:** This notebook contains _a lot_ of boilerplate code that we've worked through for you, along with a
lot of text and other information. At the same time, we ask relatively few questions and have you actually
implement relatively little. _However_, that "relatively little" can turn into quite a lot if you do not take
the time to read the notebook thoroughly and understand the code prior to diving into the final deliverables,
so we strongly encourage you to read the code end to end before beginning any of the specific questions.

## Problem 3: Learning from Noisy Labels
### Overview
In this problem, you will build on the proofs for learning from noisy labels we worked through during class. Specifically, you will be investigating the anchor-and-learn approach as well as how to leverage noisy labels at prediction time, if they're available.

### Learning Goals
Medical data is messy and true gold labels are often hard or prohibitively expensive to obtain in bulk. As a result, it is often necessary to leverage noisy labels in the training process. 
In this problem, we hope you:
1) Solidify your understanding of how training from noisy labels works,
2) Recognize scenarios in which noisy labels may be available at prediction time,
3) And understand both theoretically and intuitively why noisy labels at prediction time can lead to more accurate performance.

### Materials
The question is in a PDF here: https://drive.google.com/open?id=1RJruUIN4Tnol8k-pDMFh6auNXf5uFL_V, and you should include your answers to both parts in your PDF writeup. 

## Problem 4: Logistics
**Responses to this question are greatly appreciated but not graded in any way shape or form.**
Once you've completed this problem set, please fill out this form: https://forms.gle/hBfc2ccBW7sy5vASA and let
us know how long it took you, how easy you found it to understand and/or complete, and any other feedback you
have. Thank you!
