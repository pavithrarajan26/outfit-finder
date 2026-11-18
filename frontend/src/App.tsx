
import { useCallback, useEffect, useRef, useState } from "react";
import "./App.css";
import { analyzeOutfit } from "./api";
import ItemCard from "./components/ItemCard";
import UploadPanel from "./components/UploadPanel";
import type { OutfitItem } from "./types";

const MAX_BYTES = 5 * 1024 * 1024;
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [items, setItems] = useState<OutfitItem[] | null>(null);
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const resultsRef = useRef<HTMLElement | null>(null);

  // Clean up temporary image preview URLs.
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  // Handle image selection and validation.
  const selectFile = useCallback((selected: File) => {
    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError("Please choose a JPEG, PNG or WebP image.");
      return;
    }

    if (selected.size > MAX_BYTES) {
      setError("That image is over 5 MB. Please choose a smaller one.");
      return;
    }

    setError("");
    setItems(null);
    setSource("");
    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
  }, []);

  // Clear the selected image and results.
  function clearFile(): void {
    setFile(null);
    setPreviewUrl(null);
    setItems(null);
    setSource("");
    setError("");
  }

  // Support pasting screenshots using Cmd+V / Ctrl+V.
  useEffect(() => {
    function handlePaste(event: ClipboardEvent): void {
      const files = event.clipboardData?.files;

      if (files) {
        const pastedImage = Array.from(files).find((item) =>
          item.type.startsWith("image/")
        );

        if (pastedImage) {
          selectFile(pastedImage);
        }
      }
    }

    window.addEventListener("paste", handlePaste);

    return () => {
      window.removeEventListener("paste", handlePaste);
    };
  }, [selectFile]);

  // Scroll to results after analysis finishes.
  useEffect(() => {
    if (items !== null) {
      resultsRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [items]);

  // Analyze the uploaded outfit.
  async function handleAnalyze(): Promise<void> {
    if (!file || loading) return;

    setLoading(true);
    setError("");
    setItems(null);

    try {
      const data = await analyzeOutfit(file);

      setItems(data.items);
      setSource(data.source);
    } catch (analyzeError) {
      setError(
        analyzeError instanceof Error
          ? analyzeError.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#" aria-label="Outfit Finder home">
          <span className="brand-mark">✿</span>
          <span>
            Outfit<span className="brand-light">Finder</span>
          </span>
        </a>

        <span className="pill">Beta</span>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">SHOP ANY LOOK</p>

          <h1>
            Saw an outfit you love?
            <br />
            <span>Let’s find it.</span>
          </h1>

          <p className="hero-description">
            Upload a photo from Instagram, TikTok or Pinterest.
            We break the outfit into pieces so you can shop the look,
            or find prettier prices.
          </p>

          <div className="hero-trust">
            <span>✦ Spot every piece</span>
            <span>♡ Find similar styles</span>
            <span>✿ Save on the look</span>
          </div>
        </div>

        <UploadPanel
          previewUrl={previewUrl}
          fileName={file ? file.name : null}
          loading={loading}
          onFileSelected={selectFile}
          onClear={clearFile}
          onAnalyze={() => void handleAnalyze()}
        />
      </section>

      {error && (
        <div
          className="alert-message error-message"
          role="alert"
        >
          <strong>Something went wrong</strong>
          <span>{error}</span>
        </div>
      )}

      {items !== null && (
        <section
          className="results-section"
          ref={resultsRef}
        >
          <div className="results-heading">
            <div>
              <p className="eyebrow">YOUR LOOK</p>

              <h2>
                {items.length === 0
                  ? "No clothing found"
                  : `${items.length} piece${items.length === 1 ? "" : "s"} spotted`}
              </h2>
            </div>

            {source === "mock" && (
              <span className="pill pill-lavender">
                Demo data
              </span>
            )}
          </div>

          {source === "mock" && (
            <p className="demo-note">
              The backend is in demo mode, so these are sample items
              and don’t match your photo. Switch it to real analysis
              to see your own results.
            </p>
          )}

          {items.length === 0 ? (
            <div className="empty-state">
              <strong>
                We couldn’t spot any clothing in that photo.
              </strong>
              <span>
                Try a clearer picture where the outfit is fully visible.
              </span>
            </div>
          ) : (
            <div className="item-grid">
              {items.map((item) => (
                <ItemCard
                  key={item.id}
                  item={item}
                />
              ))}
            </div>
          )}
        </section>
      )}

      {items === null && !loading && !error && (
        <section className="empty-welcome">
          <div className="welcome-icon">✿</div>

          <h2>Your next favorite outfit starts here.</h2>

          <p>
            Add a photo above and we’ll pick out each piece.
            Product links and cheaper alternatives are coming next.
          </p>
        </section>
      )}

      <footer className="footer">
        <strong>Outfit Finder</strong>
        <span>
          A portfolio project · Product matches may vary.
        </span>
      </footer>
    </main>
  );
}

export default App;
