import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const submitObservable = (data) =>
  api.post("/observables", data);

export const fetchAnalysis = () =>
  api.get("/analysis/");
