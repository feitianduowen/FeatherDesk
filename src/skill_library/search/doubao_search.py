"""Doubao search/chat adapter."""


def run(keyword: str):
    """Open Doubao chat, type the keyword into the chat box, and submit it."""
    goto("https://www.doubao.com/chat/")
    wait_for_element("textarea.semi-input-textarea", timeout=15)

    click("textarea.semi-input-textarea")
    wait(0.5)
    fill(
        "textarea.semi-input-textarea",
        keyword,
        "textarea[placeholder*='发消息']",
        "textarea[role='textbox']",
    )
    wait(0.5)
    wait_for_element("#flow-end-msg-send", timeout=10)
    run_js(
        """async () => {
            const button = document.querySelector("#flow-end-msg-send");
            if (!button) return "send button not found";

            button.scrollIntoView({ block: "center", inline: "center" });
            for (let i = 0; i < 20; i += 1) {
                const disabled =
                    button.getAttribute("data-disabled") === "true" ||
                    button.getAttribute("aria-disabled") === "true" ||
                    button.disabled === true;
                const loading = button.getAttribute("data-loading") === "true";
                if (!disabled && !loading) break;
                await new Promise((resolve) => setTimeout(resolve, 200));
            }

            const rect = button.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            const eventOptions = {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: x,
                clientY: y,
            };

            button.dispatchEvent(new PointerEvent("pointerdown", eventOptions));
            button.dispatchEvent(new MouseEvent("mousedown", eventOptions));
            button.dispatchEvent(new PointerEvent("pointerup", eventOptions));
            button.dispatchEvent(new MouseEvent("mouseup", eventOptions));
            button.dispatchEvent(new MouseEvent("click", eventOptions));
            return "send button dispatched";
        }"""
    )
    wait(0.5)
    click("#flow-end-msg-send")
    wait(2)

    log(f"Doubao input submitted: {keyword}")
