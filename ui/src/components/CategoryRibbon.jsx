import React from "react";
import GoldDivider from "./GoldDivider";
import "../theme/theme.css";

export default function CategoryRibbon({
    category = "",
}) {
    return (
        <>
            <GoldDivider />

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                }}
            >
                <div
                    className="overlay-category"
                    style={{
                        minWidth: "240px",
                        textAlign: "center",
                    }}
                >
                    {category || "Category"}
                </div>
            </div>

            <GoldDivider />
        </>
    );
}
