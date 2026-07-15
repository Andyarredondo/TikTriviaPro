import { useCallback, useEffect, useState } from "react";
import { api } from "../services/api";

const ROW_COUNT = 10;
function makeEmptyRows(defaultEngine = "") {
  return Array.from({ length: ROW_COUNT }, (_, index) => ({
    sequence: index + 1,
    engine: defaultEngine,
    item_id: "",
  }));
}

function makeEmptyValidation() {
  return Array.from({ length: ROW_COUNT }, () => null);
}

export default function ProductionManager() {
  const [productions, setProductions] = useState([]);
  const [gameEngines, setGameEngines] = useState([]);
  const [isLoadingEngines, setIsLoadingEngines] = useState(true);
  const [engineErrorMessage, setEngineErrorMessage] = useState("");
  const [defaultEngineId, setDefaultEngineId] = useState("");
  const [selectedProductionId, setSelectedProductionId] =
    useState("");
  const [productionName, setProductionName] = useState("");
  const [items, setItems] = useState(() => makeEmptyRows(""));
  const [validationState, setValidationState] = useState(
    makeEmptyValidation
  );
  const [errorMessage, setErrorMessage] = useState("");
  const [isWorking, setIsWorking] = useState(false);

  const clearEditor = useCallback(() => {
    setProductionName("");
    setItems(makeEmptyRows(defaultEngineId));
    setValidationState(makeEmptyValidation());
  }, [defaultEngineId]);

  const refreshGameEngines = useCallback(async () => {
    setIsLoadingEngines(true);

    try {
      const list = await api.gameEngines.list();
      const normalized = Array.isArray(list) ? list : [];
      const enabled = normalized.find((engine) => engine?.enabled === true);
      const fallback = normalized[0];
      const nextDefaultEngine = (enabled?.id || fallback?.id || "");

      setGameEngines(normalized);
      setDefaultEngineId(nextDefaultEngine);
      setEngineErrorMessage("");

      setItems((current) => {
        return current.map((item) => {
          if (item.engine) {
            return item;
          }

          return {
            ...item,
            engine: nextDefaultEngine,
          };
        });
      });
    } catch (error) {
      console.error(error);
      setGameEngines([]);
      setDefaultEngineId("");
      setEngineErrorMessage(
        error.message || "Unable to load game engines."
      );
    } finally {
      setIsLoadingEngines(false);
    }
  }, []);

  const refreshProductions = useCallback(async () => {
    try {
      const list = await api.productions.list();
      setProductions(Array.isArray(list) ? list : []);
    } catch (error) {
      console.error(error);
      setProductions([]);
      setErrorMessage(
        error.message || "Unable to load productions."
      );
    }
  }, []);

  useEffect(() => {
    refreshProductions();
  }, [refreshProductions]);

  useEffect(() => {
    refreshGameEngines();
  }, [refreshGameEngines]);

  const validateProduction = useCallback(() => {
    const result = items.map((item) => {
      return item.item_id.trim().length > 0;
    });

    setValidationState(result);
    return result;
  }, [items]);

  const onItemChange = useCallback((index, field, value) => {
    setItems((current) => {
      const next = [...current];
      next[index] = {
        ...next[index],
        [field]: value,
      };
      return next;
    });

    setValidationState((current) => {
      const next = [...current];
      next[index] = null;
      return next;
    });
  }, []);

  const onValidate = useCallback(() => {
    validateProduction();
    setErrorMessage("");
  }, [validateProduction]);

  const onSave = useCallback(async () => {
    const name = productionName.trim();
    const cleanedItems = items
      .map((item, index) => ({
        sequence: index + 1,
        engine: item.engine || defaultEngineId,
        item_id: item.item_id.trim(),
      }))
      .filter((item) => item.item_id.length > 0);

    if (!name) {
      setErrorMessage("Production name is required.");
      return;
    }

    if (cleanedItems.length === 0) {
      setErrorMessage(
        "Enter at least one Item ID before saving."
      );
      return;
    }

    setIsWorking(true);

    try {
      await api.productions.create({
        production_name: name,
        items: cleanedItems,
      });

      await refreshProductions();
      setSelectedProductionId("");
      clearEditor();
      setErrorMessage("");
    } catch (error) {
      console.error(error);
      setErrorMessage(
        error.message || "Unable to save production."
      );
    } finally {
      setIsWorking(false);
    }
  }, [clearEditor, defaultEngineId, items, productionName, refreshProductions]);

  const onLoad = useCallback(async () => {
    if (!selectedProductionId) {
      setErrorMessage("Select a production to load.");
      return;
    }

    setIsWorking(true);

    try {
      const production = await api.productions.get(
        selectedProductionId
      );
      const incomingItems = Array.isArray(
        production?.items
      )
        ? production.items
        : [];

      const paddedItems = Array.from(
        { length: ROW_COUNT },
        (_, index) => {
          const loaded = incomingItems[index] || {};

          return {
            sequence: index + 1,
            engine: loaded.engine || defaultEngineId,
            item_id: loaded.item_id || loaded.board_id || "",
          };
        }
      );

      setProductionName(production?.production_name || "");
      setItems(paddedItems);
      setValidationState(makeEmptyValidation());
      setErrorMessage("");
    } catch (error) {
      console.error(error);
      setErrorMessage(
        error.message || "Unable to load production."
      );
    } finally {
      setIsWorking(false);
    }
  }, [defaultEngineId, selectedProductionId]);

  const onDelete = useCallback(async () => {
    if (!selectedProductionId) {
      setErrorMessage("Select a production to delete.");
      return;
    }

    setIsWorking(true);

    try {
      await api.productions.remove(selectedProductionId);
      await refreshProductions();
      setSelectedProductionId("");
      clearEditor();
      setErrorMessage("");
    } catch (error) {
      console.error(error);
      setErrorMessage(
        error.message || "Unable to delete production."
      );
    } finally {
      setIsWorking(false);
    }
  }, [clearEditor, refreshProductions, selectedProductionId]);

  return (
    <div className="deck-card production-manager">
      <h3>Production Manager</h3>

      {errorMessage && (
        <div className="placeholder production-message">
          {errorMessage}
        </div>
      )}

      {engineErrorMessage && (
        <div className="placeholder production-message">
          {engineErrorMessage}
        </div>
      )}

      <section className="contestant-mode production-section">
        <div className="board-control-label">
          Production Name
        </div>

        <div className="board-control-row">
          <input
            id="production-name"
            className="production-input"
            type="text"
            value={productionName}
            onChange={(event) =>
              setProductionName(event.target.value)
            }
            placeholder="Enter production name"
            disabled={isWorking}
          />
        </div>
      </section>

      <section className="contestant-mode production-section">
        <div className="board-control-label">
          Saved Productions
        </div>

        <select
          id="saved-productions"
          value={selectedProductionId}
          onChange={(event) =>
            setSelectedProductionId(event.target.value)
          }
          disabled={isWorking}
        >
          <option value="">Select a production</option>
          {productions.map((production) => (
            <option key={production.id} value={production.id}>
              {production.production_name}
            </option>
          ))}
        </select>
      </section>

      <section className="contestant-mode production-section">
        <div className="board-control-label">
          Game Item List
        </div>

        {items.map((item, index) => {
          const rowIsValid = validationState[index];
          const icon =
            rowIsValid === null
              ? "-"
              : rowIsValid
              ? "✓"
              : "✗";

          return (
            <div
              className="board-control-row production-row"
              key={`production-row-${index + 1}`}
            >
              <span className="production-sequence">
                {index + 1}
              </span>

              <select
                className="production-engine"
                value={item.engine}
                onChange={(event) =>
                  onItemChange(
                    index,
                    "engine",
                    event.target.value
                  )
                }
                disabled={isWorking || isLoadingEngines || gameEngines.length === 0}
              >
                <option value="" disabled>
                  {isLoadingEngines ? "Loading engines..." : "Select engine"}
                </option>

                {gameEngines.map((engine) => (
                  <option
                    key={engine.id}
                    value={engine.id}
                    disabled={engine.enabled !== true}
                  >
                    {engine.name}
                  </option>
                ))}
              </select>

              <input
                className="production-input"
                type="text"
                value={item.item_id}
                onChange={(event) =>
                  onItemChange(
                    index,
                    "item_id",
                    event.target.value
                  )
                }
                placeholder="Item ID (e.g. FF-000123)"
                disabled={isWorking}
              />

              <span
                className="production-validation"
                aria-label={`Row ${index + 1} validation`}
              >
                {icon}
              </span>
            </div>
          );
        })}
      </section>

      <section className="contestant-actions production-actions">
        <button
          type="button"
          onClick={onValidate}
          disabled={isWorking}
        >
          Validate
        </button>

        <button
          type="button"
          onClick={onSave}
          disabled={isWorking}
        >
          Save
        </button>

        <button
          type="button"
          onClick={onLoad}
          disabled={isWorking || !selectedProductionId}
        >
          Load
        </button>

        <button
          type="button"
          onClick={onDelete}
          disabled={isWorking || !selectedProductionId}
        >
          Delete
        </button>
      </section>
    </div>
  );
}
