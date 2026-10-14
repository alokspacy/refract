"use client";

import React from "react";
import { DALTONIZATION_MATRICES } from "@/lib/color-filters";

export function ColorblindFilterDefs() {
  return (
    <svg className="hidden" aria-hidden="true">
      <defs>
        {Object.entries(DALTONIZATION_MATRICES).map(([id, values]) => (
          <filter id={`filter-${id}`} key={id}>
            <feColorMatrix type="matrix" values={values} />
          </filter>
        ))}
      </defs>
    </svg>
  );
}
