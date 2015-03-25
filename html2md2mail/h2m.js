/* h2m.js

This bookmarklet does:

1. Take a selection in a Web page
2. Convert the DOM to MarkDown
3. Prepare an email with the content as a MultiMarkDown


Code origin:
* The DOM to MarkDown conversion is done through a piece of code which I found on [David Bengoa's gist](https://gist.github.com/YouWoTMA/1762527) but searching through GitHub, it seems it comes from the [unmarked](https://github.com/thesunny/unmarked) project by [thesunny](https://github.com/thesunny).
* The rest of the code is mine and licensed under MIT License.

Karl Dubost. MIT License.

*/

// DOM to MarkDown Code
// --------------------


// `markdownEscape` escape characters with a special meaning in MarkDown
function markdownEscape(text){
    return text.replace(/\s+/g," ").replace(/[\\*_>#]/g,"\\$&");
}

// `repeat`
function repeat(str,times){
    return (new Array(times+1)).join(str)
}

// `childsToMarkdown` to navigate the children tree
function childsToMarkdown(tree,mode){
    var res = "";
    for(var i=0, l=tree.childNodes.length; i<l; ++i){
        res += nodeToMarkdown(tree.childNodes[i], mode);
    }
    return res;
}

// `nodeToMarkdown` is the core of the conversion
function nodeToMarkdown(tree,mode){
    var nl = "\n\n";
    if(tree.nodeType == 3){ // Text node
        return markdownEscape(tree.nodeValue)
    }else if(tree.nodeType == 1){
        if(mode == "block"){
            // taking care of block tags
            switch(tree.tagName.toLowerCase()){
                case "br":
                    return nl;
                case "hr":
                    return nl + "---" + nl;
                // Block container elements
                case "p":
                case "div":
                case "section":
                case "address":
                case "center":
                    return nl + childsToMarkdown(tree, "block") + nl;
                case "ul":
                    return nl + childsToMarkdown(tree, "u") + nl;
                case "ol":
                    return nl + childsToMarkdown(tree, "o") + nl;
                case "pre":
                    return nl + "    " + childsToMarkdown(tree, "inline") + nl;
                case "code":
                    if(tree.childNodes.length == 1){
                        break; // use the inline format
                    }
                    return nl + "    " + childsToMarkdown(tree, "inline") + nl;
                case "h1": case "h2": case "h3": case "h4": case "h5": case "h6": case "h7":
                    return nl + repeat("#", +tree.tagName[1]) + "  " + childsToMarkdown(tree, "inline") + nl;
                case "blockquote":
                    return nl + "> " + childsToMarkdown(tree, "inline") + nl;
            }
        }
        if(/^[ou]+$/.test(mode)){
            if(tree.tagName == "LI"){
                return "\n" + repeat("  ", mode.length - 1) + (mode[mode.length-1]=="o"?"1. ":"- ") + childsToMarkdown(tree, mode+"l");
            }else{
                console.log("[toMarkdown] - invalid element at this point " + mode.tagName);
                return childsToMarkdown(tree, "inline")
            }
        }else if(/^[ou]+l$/.test(mode)){
            if(tree.tagName == "UL"){
                return childsToMarkdown(tree,mode.substr(0,mode.length-1)+"u");
            }else if(tree.tagName == "OL"){
                return childsToMarkdown(tree,mode.substr(0,mode.length-1)+"o");
            }
        }

        // Inline tags
        switch(tree.tagName.toLowerCase()){
            case "strong":
            case "b":
                return "**" + childsToMarkdown(tree,"inline") + "**";
            case "em":
            case "i":
                return "_" + childsToMarkdown(tree,"inline") + "_";
            case "code": // Inline version of code
                return "`" + childsToMarkdown(tree,"inline") + "`";
            case "a":
                return "[" + childsToMarkdown(tree,"inline") + "](" + tree.getAttribute("href") + ")";
            case "img":
                return nl + "[_Image_: " + markdownEscape(tree.getAttribute("alt")) + "](" + tree.getAttribute("src") + ")" + nl;
            case "script":
            case "style":
            case "meta":
                return "";
            default:
                console.log("[toMarkdown] - undefined element " + tree.tagName)
                return childsToMarkdown(tree,mode);
        }

    }
}

// `toMarkdown` output the final converted text into MarkDown
function toMarkdown(node){
    return nodeToMarkdown(node,"block").replace(/[\n]{2,}/g,"\n\n").replace(/^[\n]+/,"").replace(/[\n]+$/,"");
}

// Handling MarkDown Links
// -----------------------

// Selection of Content in Web Page
// --------------------------------

// Email Generation
// ----------------

// Web Document Parameters
// -----------------------

// `getDocTitle` returns the title of Web document
function getDocTitle() {
    return document.title;
}

// `getDocDate` returns the date of Web document
function getDocDate() {
    // TODO. Better heuristics for dates because of server badly configured
    // Maybe a way to tell the user that the date is dubious.
    return new Date(document.lastModified).toUTCString();
}

// `getDocUri` returns URI of Web document
function getDocUri() {
    return document.location;
}

// Core Program
// ------------

// we need a registry for Markdown links
var linkregistry = Object.create(null);
var docbody = '';
var doctitle = getDocTitle();
var docuri = getDocUri();
var docdate = getDocDate();
