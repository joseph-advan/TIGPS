建模前檢查輸出說明
================

目的：檢查 8 個 relationship 特徵是否適合用來分析心理健康風險分數（憂鬱總分）。
每個波次（W2, W3）各輸出 11 個檔案。

檔案說明：
01_missingness.csv：缺失值比例
02_descriptive_stats_complete_cases.csv：完整樣本描述統計
03_outlier_iqr_check.csv：IQR 離群值檢查
04_feature_target_correlations.csv：特徵與目標分數的 Pearson/Spearman
05_feature_feature_corr_pearson.csv：特徵間 Pearson 相關矩陣
06_feature_feature_corr_spearman.csv：特徵間 Spearman 相關矩陣
07_vif_check.csv：多重共線性（VIF）
08_univariate_ols.csv：單一特徵回歸（各自影響）
09_multivariate_std_beta.csv：多變量標準化係數（同時納入 8 特徵）
10_multivariate_model_metrics.csv：多變量模型 R2 / adj R2
11_pre_model_flags.csv：重點風險指標與門檻提醒

建議流程：
先看 11_pre_model_flags -> 04_feature_target_correlations -> 07_vif_check -> 09/10 模型結果。
