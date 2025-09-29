#  This file define the functions for Main.py
EMU_PER_CM = 360000  # EMU per centimeter
EMU_PER_POINT = 12700

def get_line_width(w_pt):
    if w_pt < 1:
        tikz_style = "thin"
    elif 1 <= w_pt < 2:
        tikz_style = "semithick"
    elif 2 <= w_pt < 3:
        tikz_style = "thick"
    elif 3 <= w_pt < 4:
        tikz_style = "very thick"
    else:
        tikz_style = f"line width={w_pt:.2f}pt"
    return tikz_style 

def shape_to_tikz(shape, slide_height):
    # Shape geometric to tikz object name mapping 
    # Convert position/size from EMU -> cm
    x = shape.left / EMU_PER_CM
    y = (slide_height - shape.top - shape.height) / EMU_PER_CM  # flip y-axis
    width = shape.width / EMU_PER_CM
    height = shape.height / EMU_PER_CM
    geometry = get_shape_geometry(shape)
    shape_type = shape.shape_type
    # Get shape text if available
    text = getattr(shape, "text", "")
    # Escape LaTeX special characters in text
    text = text.replace('&', r'\&').replace('%', r'\%').replace("\n","\\\\")
    
    line_width = get_line_width(shape.line.width /EMU_PER_POINT )
    tikz_cmd = gen_tikz_command(width,height,x,y,text,geometry,shape_type,shape, line_width )

    return tikz_cmd

def gen_tikz_command(width,height,x,y,text,geometry,shape_type,shape,line_width):
    tikz_cmd = ""
    match geometry:
        case "rect" : 
            if "TEXT_BOX" in str(shape_type) :
                tikz_cmd = (
                f"\\node[align = center] at ({x + width/2:.2f},{y + height/2:.2f}) {{{text}}}; \n"
                )
            elif "AUTO_SHAPE" in str(shape_type) : 
                tikz_cmd = f"\draw[{line_width}] ({x:.2f},{y:.2f}) rectangle ({x + width:.2f},{y + height:.2f}); \n "
                if text != "":
                    tikz_cmd += f"\\node[align = center] at ({x + width/2:.2f},{y + height/2:.2f}) {{{text}}}; \n"
            else :
                print("Unknown object")
                return None 

        case "ellipse" : 
            tikz_cmd = f"\draw [fill=black,{line_width}] ({x:.2f},{y:.2f}) circle (2pt);\n"
            
        case "straightConnector1" : 
                if shape.begin_x < shape.end_x :
                    tikz_cmd = (
                        f"\draw[->,{line_width}]  ({x:.2f},{y:.2f}) -- ({x + width:.2f},{y + height:.2f}) ;\n"
                        )
                else : 
                    tikz_cmd = (
                        f"\draw[<-,{line_width}]  ({x:.2f},{y:.2f}) -- ({x + width:.2f},{y + height:.2f}) ;\n"
                        )
        case "line" :
             tikz_cmd = (
                f"\draw[{line_width}]  ({x:.2f},{y:.2f}) -- ({x + width:.2f},{y + height:.2f}) ;\n"
                )
    return tikz_cmd 


def get_shape_geometry(shape):
    """
    Return the exact geometry of an AutoShape (e.g. 'rect', 'rightArrow'),
    or None if not available.
    """
    try:
        geom = shape.element.xpath(".//a:prstGeom")[0]
        return geom.attrib.get("prst")
    except IndexError:
        return None