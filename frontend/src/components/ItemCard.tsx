import type { OutfitItem } from "../types";

type ItemCardProps = {
  item: OutfitItem;
};

const KNOWN_CATEGORIES = ["top", "bottom", "dress", "outerwear", "shoes", "bag", "accessory"];

function categoryClass(category: string): string {
  const key = category.trim().toLowerCase();
  return KNOWN_CATEGORIES.includes(key) ? `cat-${key}` : "cat-other";
}

function ItemCard({ item }: ItemCardProps) {
  const percent = Math.round(item.confidence * 100);

  return (
    <article className="item-card">
      <div className="item-card-top">
        <span className={`category-chip ${categoryClass(item.category)}`}>{item.category}</span>
        <span className="item-color">{item.color}</span>
      </div>

      <h3>{item.style}</h3>
      <p className="item-description">{item.description}</p>

      <div className="confidence">
        <div className="confidence-label">
          <span>Match confidence</span>
          <strong>{percent}%</strong>
        </div>
        <div
          className="confidence-track"
          role="progressbar"
          aria-valuenow={percent}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Confidence for ${item.style}`}
        >
          <i style={{ width: `${percent}%` }} />
        </div>
      </div>

      <p className="item-query">
        <span>Search</span> {item.search_query}
      </p>
    </article>
  );
}

export default ItemCard;