import React, { useEffect } from "react";
import PropTypes from "prop-types";

function ErrorAlert({ error, clearError }) {
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 3000); // 3 seconds
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  if (!error) return null;

  return (
    <div className="alert alert-danger" role="alert">
      {error}
    </div>
  );
}

ErrorAlert.propTypes = {
  error: PropTypes.string,
  clearError: PropTypes.func.isRequired,
};

export default ErrorAlert;
