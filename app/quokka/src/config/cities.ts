import type { LatLngTuple } from "leaflet"

export type CityName = "Namur" | "Bruxelles" | "Liège" | "Charleroi"

export const citiesName = ["Namur", "Bruxelles", "Liège", "Charleroi"]
export const citiesCoordinates = {
  Namur: [50.465803, 4.857632],
  Bruxelles: [50.811494, 4.380489],
  Liège: [50.64055, 5.575204],
  Charleroi: [50.416042, 4.445956],
} as Record<CityName, LatLngTuple>

export const getCity = (cityName: CityName) => {
  return citiesCoordinates[cityName]
}
