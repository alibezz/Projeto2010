esses artigos foram coletados dia 27/07.

Peguei todos os que citam o which side are you on? que são de portais bons, como acl, acm, ieee e springer, ou de autores fodas da área q tão no citeseer (Theresa Wilson).

Não consegui baixar ainda: "Collaborative Inference of Sentiments from Texts",  Semantic Approaches to Fine and Coarse-Grained Feature-Based Opinion Mining,  Learning MultiLinguistic Knowledge for Opinion Analysis (acm), An Algorithm for Detection of Cognitive Intentionality in Text Analysis (ieee) 

       Classifying party affiliation from political
speech
IMPORTANTE

-=====> feture redundancy in perspective classification: mostra que menos às vezes dá na mesma.

6    Consolidation of perspective
We explore feature redundancy in perspective
classification.We first investigate retention of only
N best features, then elimination thereof. As a
proxy of feature quality, we use the weight as-
signed to the feature by the SVM - BOOL model                       ****** This finding is consistent with Lin
based on the training data. Thus, to get the per-     and Hauptmann (2006) study of perspective vs
formance with N best features, we take the N          topic classification: While topical differences be-
                                                   2
highest and lowest weight features, for the posi-     tween two corpora are manifested in difference in
tive and negative classes, respectively, and retrain  distributions of great many words, they observed
SVM - BOOL with these features only.8                 little perspective-based variation in distributions
                                                      of most words, apart from certain words that are
                                                      preferentially used by adherents of one or the other
Table 3: Consolidation of perspective. Nbest
                                                      perspective on the given topic. ****
shows the smallest N and its proportion out of
all features for which the performance of SVM -
BOOL with only the best N features is not sig-
nificantly inferior (p1t >0.1) to that of the full
feature set. No-Nbest shows the largest num-
ber N for which a model without N best fea-
tures is not significantly inferior to the full model.
N={50, 100, 150, . . . , 1000}; for DP and BL-I, ad-
ditionally N={1050, 1100, ..., 1500}; for PBA, ad-
ditionally N={10, 20, 30, 40}.

                           *************** For DP and BL-I datasets, the results seem
                         to suggest perspectives with more diffused key-
                         word distribution (No-NBest figures are higher).
                         We note, however, that feature redundancy exper-
                         iments are confounded in these cases by either a
                         low power of the paired t-test with only 4 pairs
                         (DP) or by a high variance in performance among
                         the 10 folds (BL-I), both of which lead to nume-
                         rically large discrepancy in performance that is not
                         deemed significant, making it easy to “match” the
Data    Nbest   No-Nbest
      N     %  N      %  full set performance with small-N best features as
                     <1%
PBA  250 2.6%  10
                         well as without large-N best features. Better com-
                     <1%
BL   500 4.9% 100
                         parisons are needed in order to verify the hypo-
     100 <1%
DP            1250 5.2%
BL-I 200 2.2% 950    11% thesis of low consolroidation. **************

Approach: comece com menos e vá botando mais palavras se necessário. Talvez aplicar um modelo que separe semanticamente as palavrasd dentro do assunto que se discute e usá-las.

