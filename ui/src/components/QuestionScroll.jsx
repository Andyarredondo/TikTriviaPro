import React from "react";
import "../theme/theme.css";

export default function QuestionScroll({
    category = "",
    question = "",
}) {
    return (
        <section className="question-scroll">
            {category && (
                <div className="question-category">
                    {category}
                </div>
            )}

            <div className="question-text">
                {question || "Question will appear here"}
            </div>
        </section>
    );
}
