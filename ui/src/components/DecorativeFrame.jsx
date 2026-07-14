import React from "react";
import "../theme/theme.css";

export default function DecorativeFrame({children}) {
    return (
        <div className="rrn-frame">
            <div className="rrn-corner tl"></div>
            <div className="rrn-corner tr"></div>
            <div className="rrn-corner bl"></div>
            <div className="rrn-corner br"></div>

            <div className="rrn-inner">
                {children}
            </div>
        </div>
    );
}
