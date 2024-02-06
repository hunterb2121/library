const hex2RGB = (hex) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    return {r, g, b};
};

const RGB2HSL = (r, g, b) => {
    r /= 255;
    g /= 255;
    b /= 255;

    const l = Math.max(r, g, b);
    const s = l - Math.min(r, g, b);
    const h = s 
        ? l === r 
            ? (g - b) / s 
            : l === g 
            ? 2 + (b - r) / s 
            : 4 + (r - g) / s 
        : 0;

    return [
        60 * h < 0 ? 60 * h + 360 : 60 * h,
        100 * (s ? (l <= 0.5 ? s / (2 * l - s) : s / (2 - (2 * l - s ))) : 0),
        (100 * (2 * l - s)) / 2,
    ];
};