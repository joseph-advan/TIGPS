# Table 3A: W3 Standardized Coefficient Comparison

Coefficients are from standardized predictors with median imputation, for model-comparison purposes.

| Feature Code | Variable | Source Type | Items | Multivariable Logistic Std. B | LASSO Logistic Std. B | Ridge Logistic Std. B | Selected by LASSO |
|---|---|---|---|---|---|---|---|
| online_activity_sum | Online Activity Sum | online_activity_sum_complete_4_items | 21-3;21-4;21-5;21-6 | 0.0130 | 0.0000 | 0.0102 | False |
| gender_Male | Gender: Male vs Female | categorical_dummy | 1 | -0.2023 | -0.1887 | -0.1805 | True |
| family_structure_Biological_father_deceased | Parental Marital Status / Family Structure: Biological father deceased vs Married, living together | categorical_dummy | 3 | -0.0126 | 0.0000 | -0.0116 | False |
| family_structure_Biological_mother_deceased | Parental Marital Status / Family Structure: Biological mother deceased vs Married, living together | categorical_dummy | 3 | -0.0072 | 0.0000 | -0.0060 | False |
| family_structure_Divorced_living_separately | Parental Marital Status / Family Structure: Divorced, living separately vs Married, living together | categorical_dummy | 3 | 0.0581 | 0.0333 | 0.0470 | True |
| family_structure_Divorced_living_together | Parental Marital Status / Family Structure: Divorced, living together vs Married, living together | categorical_dummy | 3 | 0.0168 | 0.0000 | 0.0140 | False |
| family_structure_Married_separated | Parental Marital Status / Family Structure: Married, separated vs Married, living together | categorical_dummy | 3 | 0.0050 | 0.0000 | 0.0067 | False |
| family_structure_Married_separated_due_to_work | Parental Marital Status / Family Structure: Married, separated due to work vs Married, living together | categorical_dummy | 3 | 0.0200 | 0.0000 | 0.0128 | False |
| family_structure_Other | Parental Marital Status / Family Structure: Other vs Married, living together | categorical_dummy | 3 | -0.0294 | -0.0081 | -0.0270 | True |
| family_structure_Unmarried_living_separately | Parental Marital Status / Family Structure: Unmarried, living separately vs Married, living together | categorical_dummy | 3 | 0.0541 | 0.0277 | 0.0440 | True |
| family_structure_Unmarried_living_together | Parental Marital Status / Family Structure: Unmarried, living together vs Married, living together | categorical_dummy | 3 | 0.0140 | 0.0000 | 0.0106 | False |
| 59 | Perceived Social Status (Subjective Social Status) | single_item_ordinal | 59 | 0.0615 | 0.0463 | 0.0648 | True |
| 49 | Overall Life Satisfaction | single_item_ordinal | 49 | 0.1478 | 0.1566 | 0.1600 | True |
| 50 | Recent Subjective Happiness | single_item_ordinal | 50 | 0.1250 | 0.1123 | 0.1316 | True |
| 48 | Perceived Effectiveness of School-based Digital/Technology Learning | single_item_ordinal | 48 | -0.0627 | -0.0415 | -0.0609 | True |
| 34 | Cyberbullying Victimization (including Misinformation-related) | binary | 34 | 0.0954 | 0.0853 | 0.0870 | True |
| 36 | Cyberbullying Perpetration (including Misinformation-related) | binary | 36 | 0.0427 | 0.0314 | 0.0474 | True |
| 30 | Physical/Offline Bullying Victimization | binary | 30 | 0.1095 | 0.1010 | 0.1030 | True |
| 32 | Physical/Offline Bullying Perpetration | binary | 32 | 0.0703 | 0.0678 | 0.0706 | True |
| scale_19_55 | Positive Mental Well-being (WHO-5) | multi_item_scale | 55-1;55-2;55-3;55-4;55-5 | 0.0449 | 0.0224 | 0.0424 | True |
| scale_20_52 | Self-Worth and Positive Self-Concept | multi_item_scale | 52-1;52-2;52-3 | -0.0258 | 0.0000 | -0.0269 | False |
| scale_21_39 | Delinquent and Health-Risk Behaviors | multi_item_scale | 39-1;39-2;39-3;39-4;39-5;39-6;39-7;39-8;39-9;39-10;39-11;39-12;39-13;39-14 | 0.0366 | 0.0119 | 0.0326 | True |
| scale_22_5 | Parenting Practices and Parent-Child Interaction Quality | multi_item_scale | 5-1;5-2;5-3;5-4;5-5;5-6;5-7;5-8;5-9;5-10 | -0.1751 | -0.1524 | -0.1414 | True |
| scale_23_4 | Family Cohesion and Support (Family Functioning) | multi_item_scale | 4-1;4-2;4-3;4-4;4-5;4-6 | 0.0237 | 0.0000 | -0.0061 | False |
| scale_24_29 | Problematic Internet Use and Internet Dependence | multi_item_scale | 29-1;29-2;29-3;29-4;29-5;29-6;29-7;29-8;29-9;29-10 | 0.2043 | 0.1904 | 0.1833 | True |
| scale_25_11 | Parental Involvement in Schooling and Academic Monitoring | multi_item_scale | 11-1;11-2;11-3;11-4;11-5;11-6;11-7;11-8 | -0.0679 | -0.0521 | -0.0615 | True |
| scale_26_24 | Online Coping and Support Seeking under Distress | multi_item_scale | 24-1;24-2;24-3;24-4;24-5;24-6;24-7 | 0.1646 | 0.1350 | 0.1421 | True |
| 51 | Self-Rated Health Status | single_item_ordinal | 51 | 0.5159 | 0.5020 | 0.4251 | True |
| 26_A | Social Media Self-Presentation and Online Image Management - Online Ideal Self-Presentation | decomposed_subscale | 26-1;26-2;26-3 | -0.0174 | 0.0000 | 0.0061 | False |
| 26_B | Social Media Self-Presentation and Online Image Management - Real-life Self-Satisfaction | decomposed_subscale | 26-4;26-5;26-6 | -0.0308 | -0.0067 | -0.0349 | True |
| 26_C | Social Media Self-Presentation and Online Image Management - Online-Offline Discrepancy & Immersion | decomposed_subscale | 26-7;26-8;26-9;26-10;26-11;26-12;26-13;26-14;26-15 | 0.1365 | 0.1082 | 0.1152 | True |
| 25_A | Social Media Use: Selective Sharing and Impression Management - Selective Positive Sharing | decomposed_subscale | 25-1;25-2;25-3 | -0.0489 | -0.0356 | -0.0457 | True |
| 25_B | Social Media Use: Selective Sharing and Impression Management - Digital Image Enhancement | decomposed_subscale | 25-4;25-5;25-6 | -0.0545 | -0.0117 | -0.0400 | True |
| 25_C | Social Media Use: Selective Sharing and Impression Management - Social Feedback Dependency | decomposed_subscale | 25-7;25-8;25-9 | 0.1275 | 0.0908 | 0.1108 | True |
| 27_A | Online Social Comparison and Perspective Seeking - Online Upward Social Comparison | decomposed_subscale | 27-1;27-2;27-3 | -0.0152 | 0.0000 | -0.0087 | False |
| 27_B | Online Social Comparison and Perspective Seeking - Online Perspective Seeking | decomposed_subscale | 27-4;27-5;27-6 | 0.0925 | 0.0496 | 0.0721 | True |
| 28_A | Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) - Fear of Missing Out & Social Anxiety | decomposed_subscale | 28-1;28-2;28-3 | -0.0432 | 0.0000 | -0.0309 | False |
| 28_B | Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) - Instant Response Pressure | decomposed_subscale | 28-4 | 0.0578 | 0.0000 | 0.0391 | False |
| 53_A | Social and Emotional Learning (SEL) Competencies - Self-Awareness | decomposed_subscale | 53-1;53-2;53-3;53-18 | -0.2545 | -0.1784 | -0.1807 | True |
| 53_B | Social and Emotional Learning (SEL) Competencies - Self-Management | decomposed_subscale | 53-4;53-5;53-6 | 0.2516 | 0.2072 | 0.1907 | True |
| 53_C | Social and Emotional Learning (SEL) Competencies - Motivation & Goal Setting | decomposed_subscale | 53-7;53-8;53-9 | 0.0047 | 0.0000 | 0.0212 | False |
| 53_D | Social and Emotional Learning (SEL) Competencies - Social Awareness & Relationship Skills | decomposed_subscale | 53-10;53-11;53-13;53-14;53-15 | 0.0906 | 0.0578 | 0.0825 | True |
| 53_E | Social and Emotional Learning (SEL) Competencies - Help-Seeking | decomposed_subscale | 53-12;53-16 | 0.2319 | 0.1930 | 0.1750 | True |
| 53_F | Social and Emotional Learning (SEL) Competencies - Responsible Decision-Making | decomposed_subscale | 53-17;53-19;53-20 | -0.1419 | -0.0928 | -0.1063 | True |
