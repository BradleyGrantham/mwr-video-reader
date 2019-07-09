# Modern Warfare Remastered (MWR) Video Reader

Current Pipeline
  
  * Download videos?
  * Parse videos to get lengths and scoreboards
    * Not sure how I'm going to get the scoreboards yet
        * Can use the DEFEAT and VICTORY signs as tesseract picks
        these up nicely
        * Bounding boxes are in constants
          * **Make sure these bounding boxes work 
          with more players on each team**
        * When we get a positive match, exclude frames ~10 seconds
        either side of the positive frame (exclude duplicates)
  * Send the scoreboards to textract
  * Parse the textract response
    * raw text might be best to use, looks like there's a nice ordering to it
    * Find names, kills, deaths, plants, defuses, score, map, mode
    * Should be able to work out assists as well
  * Do analysis 
  
  
## TODO 
  - [ ] Check our tesseract code works with 5 and two people scoreboards
  - [ ] Use only a top and bottom border (not side borders)
  - [ ] Is my team always on the left? Regardless 
  of if we are Opfor/Marines
  - [ ] We have only looked at two losing matches so far,
  need to make sure the bboxes work when we win
  

## Notes
  - --psm (page segmentation mode) 13 means we treat the text as a single line
  - we are going to have to use separate bounding boxes for
  different numbers of team members  