# Project: DXC ICD-10 Recommender Validation

## Overview

Thiago Bragança Carvalho contributed to the validation of a RAG-based ICD-10 recommender system at Kantonsspital Aarau.

The system generated ICD-10 diagnosis code suggestions, which were compared against SAP-coded reference diagnoses. The goal of the project was to evaluate how well the AI system could support or approximate clinical coding decisions.

This project is highly relevant to Thiago's profile because it combines:

* Healthcare AI
* Clinical AI validation
* Medical coding data
* Python-based data analysis
* Model evaluation
* RAG-based recommendation systems
* Hospital workflow understanding

## Project Context

The project took place in a hospital environment at Kantonsspital Aarau.

The AI system being evaluated generated diagnosis recommendations based on clinical information. These generated ICD-10 predictions were compared with reference codings from SAP.

The validation focused on two main diagnosis types:

* Main diagnoses
* Secondary diagnoses

Main diagnoses were evaluated mainly as a single-label prediction task, while secondary diagnoses were evaluated as a multi-label task because one case can contain several secondary diagnosis codes.

## Problem Statement

Clinical coding is complex because ICD-10 codes are highly structured and can be very specific.

A model can fail in different ways:

* It can predict the completely wrong ICD chapter.
* It can predict the correct chapter but the wrong block.
* It can predict the correct category but the wrong subcategory.
* It can predict a code that is not an exact match but is still medically or hierarchically close.
* It can miss relevant secondary diagnoses.
* It can suggest too many or too few secondary diagnoses.

Because of this, the project did not only rely on simple exact-match accuracy. It also considered hierarchical and similarity-based evaluation.

## Data Sources

The project compared two main data sources:

### SAP Reference Data

The SAP data contained the reference ICD-10 codings.

Relevant fields included:

* Case identifier
* Diagnosis type
* Reference ICD-10 code

Example conceptual fields:

* `sap_fallnr_neu`
* `coded_art`
* `coded_icd_code`

### DXC Prediction Data

The DXC data contained AI-generated ICD-10 recommendations.

Relevant fields included:

* Case identifier
* Predicted ICD-10 code
* Prediction score

Example conceptual fields:

* `fallnr`
* `dxc_icd10_code`
* `dxc_score`

## Thiago's Role

Thiago worked in a Data Science and AI Engineering context on the validation of the ICD-10 recommender system.

His work involved:

* Loading and preprocessing clinical coding data
* Comparing SAP reference codes with DXC predictions
* Evaluating model performance for main diagnoses
* Evaluating model performance for secondary diagnoses
* Working with ICD-10 hierarchy logic
* Applying exact-match and similarity-based metrics
* Creating analysis outputs and reports
* Supporting interpretation of the model's strengths and weaknesses

## Technical Responsibilities

Thiago contributed to technical work such as:

* Data cleaning
* Data preprocessing
* Case-level matching
* ICD-10 code normalization
* Comparison of true and predicted ICD-10 codes
* Metric calculation
* Chapter-level performance analysis
* Multi-label evaluation
* Result export to Excel
* Analysis of missing values
* Interpretation of model performance across ICD chapters

## Python Code Structure

The validation workflow used a modular Python codebase.

Example components included:

* `main.py`
* `data_loader.py`
* `icd_utils.py`
* `icd_tree.py`
* `metrics.py`
* `validator.py`
* `report_utils.py`

The modular structure helped separate responsibilities such as data loading, ICD utilities, metric calculation, validation logic, and report generation.

## Methods Used

The validation used several evaluation methods.

### Exact Match

Exact match checks whether the predicted ICD-10 code is exactly the same as the reference ICD-10 code.

This is a strict metric. It is useful because exact ICD-10 coding matters, but it can be too harsh when a prediction is clinically or hierarchically close.

### Top-k Evaluation

Top-k evaluation checks whether the correct ICD-10 code appears within the model's top predictions.

Important examples:

* Top-1 exact match
* Top-5 exact match

Top-5 is especially relevant for recommendation systems because the model may provide several suggestions to support a human coder.

### Hit-Rate

Hit-rate was used to measure whether at least one relevant or correct prediction was found for a case.

For main diagnoses, the hit-rate helped summarize how often the model produced at least one useful correct result.

### ICD-10 Hierarchy Evaluation

ICD-10 codes are hierarchical.

The validation considered whether predictions matched at different levels, such as:

* ICD chapter
* ICD block
* ICD category
* ICD subcategory

This helped identify whether wrong predictions were completely wrong or still close within the ICD hierarchy.

### Wu-Palmer Similarity

Wu-Palmer similarity was used to measure hierarchical similarity between ICD-10 codes.

This was useful because a prediction may not be an exact match but can still be structurally close to the reference code in the ICD hierarchy.

### Multi-Label Evaluation

Secondary diagnoses were evaluated as a multi-label prediction problem.

This required metrics such as:

* Recall
* Precision
* F1-score
* Macro averaging
* Micro averaging

This was necessary because each case can contain multiple secondary diagnoses.

## Main Diagnosis Evaluation

Main diagnoses were evaluated primarily as a single-label prediction task.

Important measured results included:

* Top-1 exact match: 21.96%
* Top-5 exact match: 45.57%
* Main diagnosis hit-rate: 49.13%

These results showed that exact prediction of the final ICD-10 code was challenging, but that the model often generated relevant suggestions within its top predictions.

## Interpretation of Main Diagnosis Results

The main diagnosis results suggest that the model had partial usefulness as a recommender system.

The Top-1 exact match showed that the first prediction was exactly correct in a limited number of cases.

The Top-5 exact match was higher, which is important because a recommender system does not necessarily need to give only one answer. If the correct code appears among the top suggestions, it can still support a human coding workflow.

The hit-rate showed that the model produced at least one correct or relevant prediction in a significant share of cases.

## Secondary Diagnosis Evaluation

Secondary diagnoses were evaluated as a multi-label task.

This was necessary because each hospital case can have several secondary diagnoses. Unlike main diagnoses, there is not always only one correct code.

The evaluation compared:

* The set of true SAP-coded secondary diagnoses per case
* The set of DXC-predicted secondary diagnoses per case

Metrics included:

* Recall
* Precision
* F1-score
* Macro-level aggregation
* Micro-level aggregation
* Chapter-level analysis

## Interpretation of Secondary Diagnosis Evaluation

The secondary diagnosis evaluation showed that model performance varied by ICD chapter.

Some chapters performed better, while others were more difficult for the system.

Examples of stronger-performing chapters included:

* Chapter 01
* Chapter 04
* Chapter 09

Examples of weaker-performing areas included:

* Chapter 07
* Chapter 08
* Chapter 12

This chapter-level variation is important because it shows that AI model performance in healthcare is not uniform across all clinical categories.

## Key Results

The most important results from the project were:

* Top-1 exact match for main diagnoses: 21.96%
* Top-5 exact match for main diagnoses: 45.57%
* Main diagnosis hit-rate: 49.13%
* Secondary diagnoses required multi-label evaluation
* Model performance varied strongly by ICD chapter
* Hierarchical similarity helped interpret non-exact predictions

## Project Deliverables

The project produced structured validation outputs such as:

* Detailed prediction comparison tables
* Main diagnosis validation results
* Secondary diagnosis evaluation tables
* Chapter-level benchmark outputs
* Similarity analysis outputs
* Excel-based reports
* Visualizations and histograms for performance interpretation

Example output files included:

* `validation_similarity_analysis.xlsx`
* `chapter_benchmark.xlsx`
* `validation_hauptdiagnose_details_all_predictions.xlsx`

## Skills Demonstrated

This project demonstrates Thiago's skills in:

* Python
* pandas
* Data preprocessing
* Data validation
* Clinical AI evaluation
* Healthcare data analysis
* ICD-10 code analysis
* Model performance evaluation
* Multi-label classification evaluation
* Metric interpretation
* Excel report generation
* Healthcare domain understanding
* Communication of AI results

## Why This Project Is Important

This project is important because it shows that Thiago has practical experience with real-world AI validation in a healthcare environment.

Unlike simple machine learning tutorial projects, this work involved:

* Real hospital context
* Clinical coding data
* Reference data comparison
* Healthcare-specific evaluation challenges
* Strict and soft performance metrics
* Interpretation of results for practical use

It demonstrates that Thiago understands that AI systems in healthcare must be evaluated carefully and quantitatively before they can be trusted or integrated into workflows.

## Relevance for AI Engineering Roles

This project is highly relevant for AI Engineering roles because it includes:

* Model evaluation
* Data processing
* Performance analysis
* Validation workflow design
* Result interpretation
* Working with real-world healthcare data
* Understanding limitations of AI recommendations

It also shows that Thiago can work on the evaluation side of AI systems, which is essential for production AI and healthcare AI.

## Relevance for Healthcare AI Roles

This project is especially relevant for healthcare AI because ICD-10 coding is a real clinical and administrative process.

The project required understanding:

* Medical coding structures
* Diagnosis code hierarchy
* Hospital data sources
* AI recommendation evaluation
* Clinical relevance of predictions
* The difference between exact correctness and hierarchical similarity

This makes the project one of Thiago's strongest examples for Healthcare AI, Medical Informatics, and clinical AI validation roles.

## Interview Explanation

If asked about this project in an interview, Thiago can explain it like this:

"I worked on the validation of a RAG-based ICD-10 recommender system at Kantonsspital Aarau. The system generated ICD-10 diagnosis suggestions, and we compared these predictions with SAP-coded reference diagnoses. My work involved Python-based data processing, ICD-10 code comparison, top-k evaluation, Wu-Palmer similarity, and chapter-level analysis. For main diagnoses, we measured a Top-1 exact match of 21.96%, a Top-5 exact match of 45.57%, and a hit-rate of 49.13%. For secondary diagnoses, we treated the problem as a multi-label evaluation using recall, precision, and F1-score. The project taught me how important careful validation is when evaluating AI systems in healthcare."

## Short Recruiter Summary

Thiago contributed to the validation of a RAG-based ICD-10 recommender system at Kantonsspital Aarau. He compared AI-generated diagnosis recommendations with SAP reference codings, evaluated main and secondary diagnoses, and used metrics such as Top-1 exact match, Top-5 exact match, hit-rate, Wu-Palmer similarity, precision, recall, and F1-score. The project demonstrates practical experience in Healthcare AI, Python-based data analysis, and clinical AI validation.

## Technical Summary

Thiago worked on a Python-based validation workflow for comparing DXC ICD-10 predictions with SAP reference codes. The evaluation included single-label main diagnosis metrics, multi-label secondary diagnosis metrics, ICD hierarchy analysis, Wu-Palmer similarity, chapter-level benchmarking, and Excel-based reporting. The work demonstrates practical AI evaluation skills in a real healthcare context.

## STAR Interview Version

### Situation

Kantonsspital Aarau needed to evaluate a RAG-based ICD-10 recommender system that generated diagnosis code suggestions.

### Task

The task was to compare the AI-generated ICD-10 predictions with SAP-coded reference diagnoses and determine how well the system performed.

### Action

Thiago worked on Python-based data loading, preprocessing, ICD-10 code comparison, main diagnosis evaluation, secondary diagnosis multi-label evaluation, top-k metrics, Wu-Palmer similarity, and chapter-level benchmarking.

### Result

The validation produced measurable results, including a Top-1 exact match of 21.96%, a Top-5 exact match of 45.57%, and a main diagnosis hit-rate of 49.13%. The analysis also showed that performance varied by ICD chapter and that hierarchical similarity was useful for interpreting near-miss predictions.

## Possible Interview Questions This File Can Answer

This file should help the chatbot answer questions such as:

* What was Thiago's DXC ICD-10 validation project?
* What did Thiago do at Kantonsspital Aarau?
* What experience does Thiago have with clinical AI validation?
* How has Thiago evaluated AI models?
* What healthcare AI experience does Thiago have?
* What metrics did Thiago use for ICD-10 evaluation?
* What is Thiago's experience with RAG systems?
* What is Thiago's experience with Python data analysis?
* Why is this project relevant for an AI Engineer role?
* Can Thiago explain a healthcare AI project in STAR format?
