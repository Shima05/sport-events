interface PaginationControlsProps {
  page: number
  pageSize: number
  canGoNext: boolean
  loading: boolean
  onPageChange: (page: number) => void
}

export const PaginationControls = ({
  page,
  pageSize,
  canGoNext,
  loading,
  onPageChange,
}: PaginationControlsProps): JSX.Element => (
  <div className="pagination">
    <div className="pagination-info">
      <span>
        Page {page} · {pageSize} per page
      </span>
    </div>
    <div className="pagination-actions">
      <button type="button" onClick={() => onPageChange(page - 1)} disabled={loading || page <= 1}>
        Previous
      </button>
      <button type="button" onClick={() => onPageChange(page + 1)} disabled={loading || !canGoNext}>
        Next
      </button>
    </div>
  </div>
)

export default PaginationControls
