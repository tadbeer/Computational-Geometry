# computational_geometry
Implementations of various computational geometry tasks


# overlaping_groups.py

Given a list of boxes, determines groups of boxes with any pair overlapping

Builds a dictionary 'box_ovs': containing groups of boxes with any pair in the group overlapping
each group contains a list of indices of boxes in that group

eg:
For a list with 10 boxes, and following overlapping pairs as per their index
(1,2),(2,6),(1,5),(7,9),(8,9)
the dictionary generated shall be as {0:[1,2,5,6],1:[7,8,9]}
