import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function formatTime(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  }).format(date);
}

export function formatDateTime(date: Date): string {
  return `${formatDate(date)} at ${formatTime(date)}`;
}

/**
 * Attempts to fetch from a URL, and if it fails, tries an alternate port
 * @param url The primary URL to fetch from (usually with port 5000)
 * @param options Fetch options
 * @returns Promise with the fetch response
 */
export async function fetchWithPortFallback(
  url: string,
  options?: RequestInit
): Promise<Response> {
  try {
    // Try the primary URL first (usually port 5000)
    return await fetch(url, options);
  } catch (error) {
    console.log('Primary fetch failed, trying alternate port:', error);
    
    // If the primary URL fails, try the alternate port (5001)
    if (url.includes('5000')) {
      const alternateUrl = url.replace('5000', '5001');
      console.log('Trying alternate URL:', alternateUrl);
      return await fetch(alternateUrl, options);
    }
    
    // If the URL doesn't contain the expected port or the alternate fetch also fails,
    // throw the original error
    throw error;
  }
}
