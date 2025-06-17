from numpy import linspace, setdiff1d

def generate_space_offset(count: int, end: int, offset: int, overlap: bool = False):
    if end<count:
        raise ValueError(f"Cannot generate {count} from {end-1} numbers")
    indx = linspace(0, end, count, dtype=int, endpoint=False)
    
    offindx = indx + offset
    if indx[-1]+offset>=end:
        #Raise proper warning here
        print("Offset too large. Excluding larger ones")
        offindx = offindx[offindx<end]

    if not overlap:
        offindx = setdiff1d(offindx, indx)
     
    return (indx, offindx)