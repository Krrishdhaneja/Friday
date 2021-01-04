import html

main_html = """
<html>
<head>
  <title>Friday - Personal Assistant</title>
  <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet"> 
  <style type="text/css">
  
  html {
    scroll-behavior: smooth;
  }
  
  @keyframes slide-up {
    0% {
      opacity: 0;
      transform: translateY(20px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  
  .arrow_box {
    animation: slide-up 0.4s ease;
    position: relative;
    background: #adadad;
    
      font-size: medium;
      font-family: 'JetBrains Mono', monospace;
      
      border-radius: 10px;
      margin: 0 15px 10px 15px;
      display: inline-block;
      max-width: 80%;
      padding-left: 20px;
      padding-right: 20px;
  }
  .arrow_box::after {
    top: 30px;
    border: solid transparent;
    content: "";
    height: 0;
    width: 0;
    position: absolute;
    pointer-events: none;

    margin-top: -30px;
    
    width: 0px;
    -webkit-transform:rotate(360deg);
    border-style: solid;
  }
  
  .left {
    background: #adadad;  
    border-top-left-radius: 0;
  }
  .left::after {
    right: 100%;
    border-color: transparent #adadad transparent;

    border-width: 0 20px 20px 0;
  }
  
  .right {
    float: right;
    background: #4590FF;  
    border-top-right-radius: 0;
  }
  .right::after {
    right: 0;
    border-color: #4590FF transparent transparent;
    margin-right: -20px;
    border-width: 20px 20px 0 0;
  }
  </style>
</head>

<body>
</body>
</html>
"""

speech_bubble_base = """
            var elemDiv = document.createElement('div');
            elemDiv.innerHTML = '<p>%s</p>'
            elemDiv.className = 'arrow_box %s';
            document.body.appendChild(elemDiv);
            document.body.appendChild(document.createElement('br'));
                
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
             """


def speech_bubble_left(text):
    return speech_bubble_base % (html.escape(text), "left")


def speech_bubble_right(text):
    # we add some extra <br/> tags as otherwise speech bubbles below the right aligned one aren't positioned properly
    return (speech_bubble_base % (html.escape(text), "right")) + "document.body.appendChild(document.createElement('br'));" * 3
