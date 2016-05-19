# argessay_ACL2016
Annotation Data and code for the ACL2016 paper

Data:
This zip file contains argument annotations for 115 TOEFL Essays collected from the 
corpus - TOEFL11: A Corpus of Non-Native English (http://www.ets.org/research/policy_research_reports/publications/report/2013/jrkv).
You can collect the actual corpus from LDC - https://catalog.ldc.upenn.edu/LDC2014T06.

The TOEFL11 contains eight test-prompts (i.e., questions for writing persuasive essays) where as we 
have annotated essays from prompt P1 and P3. The data in the prompts are split into two subdirectories - 
"dev" and "train". Each subdirectory in turn contains three folders - "high", "medium", "low" to 
show the scores that the essays have received.

Annotation:

The annotations follow a specific guideline of argument annotations (identifying argument components 
and relations) and the guideline can be collected from the following link:
https://www.ukp.tu-darmstadt.de/data/argumentation-mining/argument-annotated-essays/  

You can also read the following paper from Christian Stab and Iryna Gurevych to learn more about
the specific annotation guideline.

Christian Stab and Iryna Gurevych (2014)
Annotating Argument Components and Relations in Persuasive Essays. 
In: Proceedings of the the 25th International Conference on Computational 
Linguistics (COLING 2014), p.1501-1510, Ireland, Dublin.

The annotation has been conducted by "brat rapid annotation tool". Collect the tool from the 
following link: http://brat.nlplab.org/

Use:
These annotations can be used as any argumentation/discourse relation identification research.

If you use this data please cite:

@InProceedings{2016:ACL,
  author    = {Ghosh, Debanjan  and  Khanam, Aquila  and  Han, Yubo  and  Muresan, Smaranda},
  title     = {Coarse-grained Argumentation Features for Scoring Persuasive Essays},
  booktitle = {Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics},
  month     = {August},
  year      = {2016},
  address   = {Berlin, Germany},
  publisher = {Association for Computational Linguistics}
}

Note: We will be adding more annotations to this space so keep checking.
