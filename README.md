# break-captchas
Using PIL  to process the  captchas covered  basic image processing algorithms 
Using Cosine similarity (余弦相似性） to  recongize the captcha


### Common  Image Processing Algorithm
- Binaryzation (binaryzation.py  b_process)
- Cfs Cutting ( split_captha.py  get_cfs_cutting_list )
- Projection Cutting  (Split_captha.py  get_shadow_cutting_list)
- Noise Reduction algorithms (8领域消噪 reduce_noise.py depoint）

### Processing
- run the  the  process_all function of  processor.py 
- Move the generated images(elements directory) to  correspond  subdirectory of iconset directory
- Begin to  recongize the captchas  in will_check directoy , 
- For for  convenience ,I just combine the captchas to a image will_checked_combined.png

### Key point
- we recommand  use  cfs cutting  in this example  , it effectively reduce overlap  
- Cosine similarity algorithm 
