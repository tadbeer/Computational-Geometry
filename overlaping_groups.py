from numba import jit
import numpy as np
import cv2

def check_overlap(box1,box2,min_dist=-5):
    """
    input: two boxes
    output: True if both boxes overlap or the smallest manhattan distance betwwen any two corners is greater than negative of 'min_dist'
    box1 = x1,y1,w,h
    box2 = x1,y1,w,h
    min_dist = negative of maximum distance allowed between two boxes
    negative to be taken since this algorithim estimates the distance between tow boxes which actually overlap, in which case the distance would be greater than or equal to 0
    """
    return( min(box2[3]+box2[1],box1[3]+box1[1]) - max(box2[1],box1[1]) >= min_dist and min(box2[2]+box2[0],box1[2]+box1[0]) - max(box2[0],box1[0]) >= min_dist )

def clubed_box(boxes,indices):
    """
    input: a list of boxes, a list of indices of elements of this list
    output: cordinates of envelope rectangle of the boxes at given indices
    """
    ov_boxes = np.array(np.array(boxes)[indices])
    #converting x1,y1,,w,h to x1,y1,x2,y2
    ov_boxes[:,2]+=ov_boxes[:,0]
    ov_boxes[:,3]+=ov_boxes[:,1]
    #calculating clubbed box in thw format x1,y1,w,h
    return([min(ov_boxes[:,0]), min(ov_boxes[:,1]), max(ov_boxes[:,2])-min(ov_boxes[:,0]), max(ov_boxes[:,3])-min(ov_boxes[:,1]) ])

def draw_rect(img, boxes, colr, thikness=2):
    """
    boxes = [ [x1,y1,w,h], ... ]
    """
    for box in boxes:
        img = cv2.rectangle(img, (box[0],box[1]), (box[0]+box[2],box[1]+box[3]),colr,thikness)
    return (img)

# @jit
def club_overlap(boxes, frame=None):
    """
    input: list of boxes
    output: list of overlapping boxes clubbed together to form new boxes

    box list format : [ [x1,y1,w,h], ... ]
    
    given a list of boxes,
    builds a dictionary 'box_ovs': containing groups of boxes with any pair in the group overlapping
    each group contains a list of indices of boxes in that group

    eg:
    for a list with 10 boxes, and following overlapping pairs as per their index
    (1,2),(2,6),(1,5),(7,9),(8,9)
    the dictionary generated shall be as {0:[1,2,5,6],1:[7,8,9]}

    """
    if not len(boxes):
        return([])

    box_ovs = {}                                                                                #dictionary to hold groups of boxes which have any pair overlapping
    for box1_ind in range(len(boxes)):                                                          #iterating in list of boxes to be treated as first box to check overlpa with
        if sum([box1_ind in box_ovs[ov_key] for ov_key in box_ovs])>0:                          #checking if this box is part of an already determined group of overlapping boxes
            continue                                                                            #skipping further analysis wrt this box if above is true
        current_overlap_exists = False                                                          #a variable determining if given first box has generated a group of overlapping boxes
        for box2_ind in range(box1_ind+1,len(boxes)):                                           #iterating in rest of list of boxes to be treated as second box to check overlap with
            if sum([box2_ind in box_ovs[ov_key] for ov_key in box_ovs])>0:                      #checking if this box is part of an already determined group of overlapping boxes
                continue                                                                        #skipping further analysis wrt this box if above is true
            if not current_overlap_exists:                                                      #if first box hasnt generated a group of overlapping boxes
                if check_overlap(boxes[box1_ind],boxes[box2_ind]):                              #checking if first and currect second box overlap
                    current_overlap_exists = True                                               #updating the variable
                    current_overlap_index = len(box_ovs)                                        #generating an index for a new group of overlapping boxes
                    box_ovs[current_overlap_index]=[]                                           #generating a new dictionary entry for this group
                    box_ovs[current_overlap_index].append(box1_ind)                             #appending index of first box to group
                    box_ovs[current_overlap_index].append(box2_ind)                             #appending index of second box to group


            else:                                                                               #if given first box has already generated a group of overlapping boxes

                if sum([ check_overlap(boxes[box_ind], boxes[box2_ind]) for box_ind in box_ovs[current_overlap_index] ]) > 1:

                                                                                                #checking the current second box with each box in the current group for overlap
                    box_ovs[current_overlap_index].append(box2_ind)

    if not len(box_ovs):
        return([])

    # print('\n',box_ovs)
    boxes_clubbed = [clubed_box(boxes,box_ovs[ov_key]) for ov_key in box_ovs]

    return(boxes_clubbed)

    """
    #helper script to visualise implememntaion of above algorithim
    frame = draw_rect(frame,boxes,(255,255,255),3)
    frame = draw_rect(frame,boxes_clubbed,(0,0,255),2)
    img = frame
    for ov_key in box_ovs:
        clubbed_box = boxes_clubbed[ov_key]
        img = cv2.putText(img, str(ov_key),(clubbed_box[0],clubbed_box[1]-30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),4)
        img = cv2.putText(img, str(ov_key),(clubbed_box[0],clubbed_box[1]-30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        for consti_box_ind in box_ovs[ov_key]:
            consti_box = boxes[consti_box_ind]
            img = cv2.putText(img, str(ov_key),(consti_box[0],consti_box[1]-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),4)
            img = cv2.putText(img, str(ov_key),(consti_box[0],consti_box[1]-15),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    cv2.imshow('0',img)
    cv2.waitKey(0)

    """