import { useRef, useState, type ChangeEvent, type DragEvent, type KeyboardEvent } from "react";

type UploadPanelProps = {
  previewUrl: string | null;
  fileName: string | null;
  loading: boolean;
  onFileSelected: (file: File) => void;
  onClear: () => void;
  onAnalyze: () => void;
};

function UploadPanel({
  previewUrl,
  fileName,
  loading,
  onFileSelected,
  onClear,
  onAnalyze,
}: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function openFilePicker(): void {
    inputRef.current?.click();
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    const file = event.target.files?.[0];
    if (file) onFileSelected(file);
    // Reset so choosing the same file twice still triggers a change.
    event.target.value = "";
  }

  function handleDrop(event: DragEvent<HTMLDivElement>): void {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files?.[0];
    if (file) onFileSelected(file);
  }

  function handleKeyDown(event: KeyboardEvent<HTMLDivElement>): void {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openFilePicker();
    }
  }

  return (
    <div className="upload-card">
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        className="visually-hidden"
        onChange={handleInputChange}
        aria-label="Upload an outfit photo"
      />

      {previewUrl ? (
        <div className="preview">
          <img src={previewUrl} alt="Your uploaded outfit" />
          <div className="preview-footer">
            <span className="preview-name" title={fileName ?? ""}>
              {fileName}
            </span>
            <button type="button" className="text-button" onClick={onClear} disabled={loading}>
              Remove
            </button>
          </div>
        </div>
      ) : (
        <div
          className={`dropzone ${dragging ? "dragging" : ""}`}
          role="button"
          tabIndex={0}
          onClick={openFilePicker}
          onKeyDown={handleKeyDown}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          <span className="dropzone-icon">♡</span>
          <strong>Drop an outfit photo here</strong>
          <span>or click to browse · you can also paste a screenshot</span>
          <small>JPEG, PNG or WebP · up to 5 MB</small>
        </div>
      )}

      <button
        type="button"
        className="primary-button"
        onClick={onAnalyze}
        disabled={!previewUrl || loading}
      >
        {loading ? (
          <>
            <span className="spinner" /> Analyzing outfit...
          </>
        ) : (
          "Find this look  →"
        )}
      </button>
    </div>
  );
}

export default UploadPanel;