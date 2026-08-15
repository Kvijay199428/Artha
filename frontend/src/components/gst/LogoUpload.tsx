import { useState, useRef } from 'react';

interface LogoUploadProps {
  currentLogoUrl?: string | null;
  onFileSelect?: (file: File) => void;
  onRemove?: () => void;
  disabled?: boolean;
  companyName?: string;
}

export function LogoUpload({ currentLogoUrl, onFileSelect, onRemove, disabled }: LogoUploadProps) {
  const [preview, setPreview] = useState<string | null>(currentLogoUrl || null);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setError(null);
    
    // Validate type
    const allowed = ['image/png', 'image/jpeg', 'image/webp'];
    if (!allowed.includes(file.type)) {
      setError('Please upload a PNG, JPEG, or WebP image');
      return;
    }
    
    // Validate size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be less than 5MB');
      return;
    }
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        if (img.width < 100 || img.height < 100) {
          setError('Image must be at least 100×100 pixels');
          return;
        }
        setPreview(e.target?.result as string);
        onFileSelect?.(file);
      };
      img.src = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div className="flex flex-col items-start gap-3">
      {/* Preview box */}
      <div
        className={`relative w-24 h-24 rounded-lg border-2 border-dashed flex items-center justify-center overflow-hidden transition-colors cursor-pointer ${
          dragOver ? 'border-blue-400 bg-blue-50' : 'border-input bg-muted hover:border-input'
        } ${disabled ? 'opacity-60 cursor-not-allowed' : ''}`}
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        {preview ? (
          <img src={preview} alt="Company logo" className="w-full h-full object-cover" />
        ) : (
          <div className="text-center p-2">
            <svg className="w-8 h-8 text-muted-foreground mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-xs text-muted-foreground mt-1 block">Logo</span>
          </div>
        )}
      </div>
      
      <div className="flex flex-col gap-1.5">
        <button
          type="button"
          disabled={disabled}
          onClick={() => !disabled && inputRef.current?.click()}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {preview ? 'Change Logo' : 'Upload Logo'}
        </button>
        {preview && onRemove && (
          <button
            type="button"
            disabled={disabled}
            onClick={() => { setPreview(null); onRemove(); }}
            className="text-sm text-red-500 hover:text-red-600 disabled:opacity-60"
          >
            Remove Logo
          </button>
        )}
        <p className="text-xs text-muted-foreground">
          Square image recommended<br />
          PNG, JPEG or WebP · Min 100×100px · Max 5MB<br />
          Will be standardized to 600×600px
        </p>
      </div>
      
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg,image/webp"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />
    </div>
  );
}
