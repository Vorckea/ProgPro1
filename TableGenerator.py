def make_markdown_table(array):
    """ Input: Python list with rows of table as lists
               First element as header. 
        Output: String to put into a .md file 
        
    Ex Input: 
        [["Name", "Age", "Height"],
         ["Jake", 20, 5'10],
         ["Mary", 21, 5'7]] 
    """
    
    nl = "\n"

    markdown = nl
    markdown += f"| {' | '.join(array[0])} |"

    markdown += nl
    markdown += f"| {' | '.join(['---']*len(array[0]))} |"

    markdown += nl
    for entry in array[1:]:
        markdown += f"| {' | '.join(entry)} |{nl}"

    return markdown