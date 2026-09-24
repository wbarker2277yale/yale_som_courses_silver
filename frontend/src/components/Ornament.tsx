/**
 * Soane's ornamental vocabulary, drawn in markup.
 *
 * Soane worked by incision rather than moulding: grooves cut into flat plaster,
 * paterae at the intersections, a Greek fret where a cornice would otherwise be,
 * and an anthemion (Greek honeysuckle) as the terminating acroterion.
 */

/** A running Greek fret — the meander Soane ran below his cornices. */
export function FretBand({ height = 18 }: { height?: number }) {
  return (
    <svg
      className="fret"
      height={height}
      width="100%"
      role="presentation"
      aria-hidden="true"
      fill="none"
    >
      <defs>
        <pattern id="meander" width="30" height="18" patternUnits="userSpaceOnUse">
          {/* one unit of the Greek key, turned back on itself */}
          <path
            d="M1 16V2h20v12H9V6h8"
            stroke="var(--brick)"
            strokeWidth="1.3"
            fill="none"
          />
          <path d="M21 16h9" stroke="var(--brick)" strokeWidth="1.3" fill="none" />
        </pattern>
      </defs>
      <rect width="100%" height={height} fill="url(#meander)" opacity="0.55" />
    </svg>
  )
}

/**
 * A section through a saucer dome on pendentives, lit by a lantern above —
 * the device Soane used at Dulwich's mausoleum and at the Bank of England.
 */
export function SaucerDome() {
  return (
    <svg
      className="dome"
      width="260"
      height="104"
      viewBox="0 0 260 104"
      role="img"
      aria-label="Section through a saucer dome lit by a lantern"
      fill="none"
    >
      {/* daylight falling from the lantern to the gallery floor */}
      <path d="M120 34 L74 99 H186 L140 34 Z" fill="var(--lantern)" opacity="0.9" />

      {/* the lantern above the oculus, with its glazing bars */}
      <path d="M120 22 L130 12 L140 22" stroke="var(--brick)" strokeWidth="1.3" />
      <rect
        x="120"
        y="22"
        width="20"
        height="9"
        fill="var(--soane-yellow)"
        fillOpacity="0.45"
        stroke="var(--brick)"
        strokeWidth="1.3"
      />
      <path d="M127 22v9M133 22v9" stroke="var(--brick)" opacity="0.4" />

      {/* the saucer dome: shallow, segmental, coffered */}
      <path d="M56 68 A 74 37 0 0 1 204 68" stroke="var(--brick)" strokeWidth="1.5" />
      <path d="M70 68 A 60 28 0 0 1 190 68" stroke="var(--stone)" />

      {/* coffering — incised radiating lines, not modelled panels */}
      <path
        d="M84 52 L92 68M106 40 L110 68M130 35 L130 68M154 40 L150 68M176 52 L168 68"
        stroke="var(--stone)"
      />

      {/* the cornice the dome springs from, incised twice */}
      <path d="M40 68h180" stroke="var(--brick)" strokeWidth="1.5" />
      <path d="M40 72h180" stroke="var(--stone)" />

      {/* pendentives carrying the dome down to the piers */}
      <path d="M56 68 Q 60 86 76 88M204 68 Q 200 86 184 88" stroke="var(--stone)" />

      {/* piers and floor */}
      <path d="M56 99V72M76 99V88M184 99V88M204 99V72" stroke="var(--stone)" />
      <path d="M16 99h228" stroke="var(--brick)" strokeWidth="1.3" opacity="0.55" />
    </svg>
  )
}

/** The anthemion — Greek honeysuckle, Soane's habitual acroterion. */
export function Anthemion({ width = 72 }: { width?: number }) {
  return (
    <svg
      width={width}
      height={width * 0.47}
      viewBox="0 0 72 34"
      role="presentation"
      aria-hidden="true"
      fill="none"
      stroke="var(--brick)"
      strokeWidth="1.2"
    >
      {/* the palmette: a central petal with three pairs fanning out */}
      <path d="M36 29V6" />
      <path d="M36 29C33 19 29 12 23 7" />
      <path d="M36 29c3-10 7-17 13-22" />
      <path d="M36 29C31 21 24 16 14 13" />
      <path d="M36 29c5-8 12-13 22-16" />
      {/* volutes where the palmette meets its stem */}
      <path d="M30 29c-4 1-7-1-7-4s4-4 5-1" opacity="0.7" />
      <path d="M42 29c4 1 7-1 7-4s-4-4-5-1" opacity="0.7" />
      <circle cx="36" cy="29" r="1.6" fill="var(--brick)" stroke="none" />
      <path d="M2 32h68" stroke="var(--stone)" strokeWidth="1" />
    </svg>
  )
}
