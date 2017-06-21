this is where we maintain the todo


##Todos
http://mklab.iti.gr/files/csvt11_preprint.pdf


#Todos
*index of cutfiles and whether it's complete or not
*get a decent definition of a program. commercials may exist within the same program. for e.g. news -> commercial -> short weather news -> commercial should this count? (e.g. 2006-06-13_0000_US_00000433_V5_MB13_VHS14_H1_MS.txt3 ~3h15m)
* file index (cutpoints, caption avaiable)
*shortage of labelled samples: build a decent working classifier (that achieves 90+%) and let it generate samples. The supervising samples are considered labelled but extremely noisy so a noise-robust DNN model can learn from it.
*noise (consistent, e.g 2006-06-13_v11)
*just take this a single-frame image classification task? (but a stack of frames as input)
*massive model -> how to reduce its size ... and apply a simpler model



#Related Work

##important 
best performing CRF and nice summary of features used
http://lxie.nwpu-aslp.org/papers/2012-IEICE-WangXX-A2-SCI-EI-JNL.pdf

useful handcrafted features are listed:
http://www1.cs.columbia.edu/~smaskey/candidacy/cand_papers/merlino_navigation_story_seg.pdf

https://pdfs.semanticscholar.org/41ed/c1f04cef2af8aa112642a0d3fdc36a395dda.pdf
the appearance of an anchor person, audio pitch jump and significant audio pauses

Hsu et al. used a maximum entropy objective to select the most informative mid-level audio and video features and demonstrated an optimal feature fusion method. 
http://www.ee.columbia.edu/ln/dvmm/publications/03/icme2003pr.pdf

nice summary of related work
http://crcv.ucf.edu/papers/civr2005_zhai.pdf

pretty recent and relevant
http://cs229.stanford.edu/proj2012/DaneshiYu-BroadcastNews%20StoryBoundaryDetectionUsingVisual,AudioAndTextFeatures.pdf

nice
https://www.hindawi.com/journals/ijdmb/2012/732514/

automatic speaker diarization (segmenting audio based on speaker identities)
http://www.quaero.org/media/files/bibliographie/bredin_segmentation_of_tv_icassp2012.pdf

a lot of relevant papers
http://mklab.iti.gr/publications

object-level detection using caffe
https://arxiv.org/abs/1504.06201

Deeplearning
https://arxiv.org/pdf/1601.07754.pdf

CNN
https://arxiv.org/pdf/1705.08214.pdf
http://imagelab.ing.unimore.it/imagelab/pubblicazioni/2015ACMM_Scenes.pdf

Large-scale, Fast and Accurate Shot Boundary Detection through Spatio-temporal Convolutional Neural Networks
https://arxiv.org/abs/1705.03281v1

speaker identification
https://arxiv.org/abs/1507.04831v1

##not sure
features selection/fusion for commercial detection
https://arxiv.org/abs/1507.01209v1


Fusing Audio, Textual and Visual Features for Sentiment Analysis of News Videos
https://arxiv.org/abs/1604.02612v1

Key Phrase Extraction of Lightly Filtered Broadcast News
https://arxiv.org/abs/1306.4890v1


3d cnn
http://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Ng_Beyond_Short_Snippets_2015_CVPR_paper.pdf

SBD using CNN
https://arxiv.org/abs/1705.08214

topic-based segmentation and indexation of audio transcripts
http://www.inesc-id.pt/pt/indicadores/Ficheiros/1146.pdf

SVM, boosting
http://www.ee.columbia.edu/ln/dvmm/publications/04/hsu04generative.pdf

In later works, Hsu et al.  investigated alternative discriminative models, i.e. Support Vector Machine (SVM), and showed a performance improvement when combining maximum entropy with SVM.
http://www.ee.columbia.edu/~lyndon/pubs/spie2004-seg.pdf

Gao et al. [7] combined syntactic and semantic methods for segmentation using an unsupervised learning method.
http://mmlab.ie.cuhk.edu.hk/archive/2002/CSVT02_Video.pdf

used CNN to generate tags
http://medialab.sjtu.edu.cn/publications/2015/2015_BMSB_Wenjing.pdf

used ANN to do SBD
https://github.com/MaxReimann/Shot-Boundary-Detection/blob/master/paper/SBD-Approach-Paper.pdf

maximum figure-of-meritlearning approach
http://www.mirlab.org/conference_papers/International_Conference/ICASSP%202009/pdfs/0001957.pdf

novel shot boundary detection
http://www.cai.sk/ojs/index.php/cai/article/viewFile/185/156

definition of scenee
http://videoanalysis.org/Prof._Dr._Rainer_Lienhart/Publications_files/MTAP2001.pdf

scene segmentation metrics
http://mklab.iti.gr/files/csvt12_preprint.pdf

##not important
http://www.cs.cmu.edu/~mehrbod/SSeg07.pdf

https://pdfs.semanticscholar.org/5c21/6db7892fa3f515d816f84893bfab1137f0b2.pdf
existence of blank frames 

http://www.cs.cmu.edu/~mychen/publication/duygulu_ICME04.pdf
existence of blank frames


https://books.google.co.kr/books?id=nCnSy5XXdygC&pg=PA361&lpg=PA361&dq=boundary+segmentation+detection+news+program&source=bl&ots=mxpZjNw_d6&sig=JsdarYROgzMCxP_ssi8vlwqRrSA&hl=en&sa=X&ved=0ahUKEwjkzKe4yKvUAhWBkJQKHaizD_cQ6AEIYTAJ#v=onepage&q=boundary%20segmentation%20detection%20news%20program&f=false

http://mmlab.ie.cuhk.edu.hk/archive/2002/CSVT02_Video.pdf
http://www.cstr.ed.ac.uk/downloads/publications/2000/asr2000.pdf
http://www.bcs.org/upload/pdf/ewic_im99_paper3.pdf
##reference implementations
### semantic image segmentation
https://github.com/gberta/HFL_code

### shot and scene detection

*http://mklab.iti.gr/project/video-shot-segm
*https://github.com/Breakthrough/PySceneDetect
*http://johmathe.name/shotdetect.html

### shot and key frame generation
*https://github.com/yahoo/hecate
*https://github.com/andrefaraujo/videosearch

