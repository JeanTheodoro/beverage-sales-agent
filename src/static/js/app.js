/* =========================================================
   BAR DO JAUM — APPLICATION JAVASCRIPT
   ========================================================= */


/* =========================================================
   API CONFIGURATION
   ========================================================= */

const API_CONFIG = {
    baseUrl: "",

    orders: {
        list: "/admin/orders/",
        details: (orderId) => `/admin/orders/${encodeURIComponent(orderId)}/details`,
        status: (orderId) => `/admin/orders/${encodeURIComponent(orderId)}/status`
    },

    whatsapp: {
        webhook: "/whatsapp/webhook"
    },

    admin: {
        dashboard: "/admin/dashbord"
    },

    messages: {
        list: "/admin/orders/messages"
    }
};


/* =========================================================
   DOM
   ========================================================= */

const DOM = {

  connectionDot:
    document.getElementById("connectionDot"),

  connectionText:
    document.getElementById("connectionText"),

  ordersTabButton:
    document.getElementById("ordersTabButton"),

  simulatorTabButton:
    document.getElementById("simulatorTabButton"),

  adminTabButton:
    document.getElementById("adminTabButton"),

  messagesTabButton:
    document.getElementById("messagesTabButton"),

  ordersView:
    document.getElementById("ordersView"),

  simulatorView:
    document.getElementById("simulatorView"),

  adminView:
    document.getElementById("adminView"),

  messagesView:
    document.getElementById("messagesView"),

  ordersCount:
    document.getElementById("ordersCount"),

  refreshOrdersButton:
    document.getElementById("refreshOrdersButton"),

  ordersBoard:
    document.getElementById("ordersBoard"),

  simulatorMessages:
    document.getElementById("simulatorMessages"),

  simulatorEmptyState:
    document.getElementById("simulatorEmptyState"),

  simulatorPhone:
    document.getElementById("simulatorPhone"),

  simulatorPhoneHint:
    document.getElementById("simulatorPhoneHint"),

  simulatorInput:
    document.getElementById("simulatorInput"),

  sendSimulatorButton:
    document.getElementById("sendSimulatorButton"),

  simulatorEndpoint:
    document.getElementById("simulatorEndpoint"),

  simulatorHttpStatus:
    document.getElementById("simulatorHttpStatus"),

  simulatorRequest:
    document.getElementById("simulatorRequest"),

  simulatorResponse:
    document.getElementById("simulatorResponse"),

  clearSimulatorButton:
    document.getElementById("clearSimulatorButton"),

  orderModal:
    document.getElementById("orderModal"),

  modalOrderTitle:
    document.getElementById("modalOrderTitle"),

  modalOrderContent:
    document.getElementById("modalOrderContent"),

  closeOrderModalButton:
    document.getElementById("closeOrderModalButton"),

  conversationModal:
    document.getElementById("conversationModal"),

  conversationModalTitle:
    document.getElementById("conversationModalTitle"),

  conversationModalContent:
    document.getElementById("conversationModalContent"),

  closeConversationModalButton:
    document.getElementById("closeConversationModalButton"),

  settingsButton:
    document.getElementById("settingsButton"),

  settingsOverlay:
    document.getElementById("settingsOverlay"),

  settingsBackdrop:
    document.getElementById("settingsBackdrop"),

  closeSettingsButton:
    document.getElementById("closeSettingsButton"),

  saveSettingsButton:
    document.getElementById("saveSettingsButton"),

  apiBaseInput:
    document.getElementById("apiBaseInput"),

  autoRefreshInput:
    document.getElementById("autoRefreshInput"),


  /* =========================================================
     ADMINISTRATIVO
     ========================================================= */

  refreshAdminButton:
    document.getElementById("refreshAdminButton"),

  adminStartDate:
    document.getElementById("adminStartDate"),

  adminEndDate:
    document.getElementById("adminEndDate"),

  adminTodayButton:
    document.getElementById("adminTodayButton"),

  adminSevenDaysButton:
    document.getElementById("adminSevenDaysButton"),

  adminThirtyDaysButton:
    document.getElementById("adminThirtyDaysButton"),

  adminPeriodLabel:
    document.getElementById("adminPeriodLabel"),

  adminLoading:
    document.getElementById("adminLoading"),

  adminError:
    document.getElementById("adminError"),

  adminErrorMessage:
    document.getElementById("adminErrorMessage"),

  adminDashboardContent:
    document.getElementById("adminDashboardContent"),

  adminTotalOrders:
    document.getElementById("adminTotalOrders"),

  adminTotalRevenue:
    document.getElementById("adminTotalRevenue"),

  adminAverageTicket:
    document.getElementById("adminAverageTicket"),

  adminTopProductsCount:
    document.getElementById("adminTopProductsCount"),

  adminProductsTableBody:
    document.getElementById("adminProductsTableBody"),

  adminProductsMobile:
    document.getElementById("adminProductsMobile"),

  adminQuantityChart:
    document.getElementById("adminQuantityChart"),

  adminRevenueChart:
    document.getElementById("adminRevenueChart"),

  adminLastUpdate:
    document.getElementById("adminLastUpdate"),


  /* =========================================================
     MENSAGENS
     ========================================================= */

  messagesStartDate:
    document.getElementById("messagesStartDate"),

  messagesEndDate:
    document.getElementById("messagesEndDate"),

  messagesLimit:
    document.getElementById("messagesLimit"),

  refreshMessagesButton:
    document.getElementById("refreshMessagesButton"),

  messagesLoading:
    document.getElementById("messagesLoading"),

  messagesError:
    document.getElementById("messagesError"),

  messagesErrorMessage:
    document.getElementById("messagesErrorMessage"),

  messagesTableBody:
    document.getElementById("messagesTableBody"),

  messagesEmpty:
    document.getElementById("messagesEmpty"),
};


/* =========================================================
   HELPERS
   ========================================================= */

function escapeHtml(value) {

  if (
    value === null ||
    value === undefined
  ) {

    return "";
  }

  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


function formatCurrency(value) {

  const number = Number(value ?? 0);

  return new Intl.NumberFormat("pt-BR", {

    style: "currency",

    currency: "BRL",

  }).format(
    Number.isFinite(number) ? number : 0
  );
}


function formatDate(value) {

  if (!value) {

    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {

    return String(value);
  }

  return new Intl.DateTimeFormat(
    "pt-BR",
    {
      dateStyle: "short",
      timeStyle: "short",
    }
  ).format(date);
}


function normalizeApiBase(value) {

  return String(value || "")
    .trim()
    .replace(/\/+$/, "");
}


function buildApiUrl(path) {

  const baseUrl =
    normalizeApiBase(
      OrdersModule.apiBase ||
      localStorage.getItem(
        "barJaumApiBase"
      ) ||
      API_CONFIG.baseUrl
    );

  if (!baseUrl) {

    return path;
  }

  if (
    String(path).startsWith("http://") ||
    String(path).startsWith("https://")
  ) {

    return path;
  }

  return `${baseUrl}${path}`;
}


async function parseResponse(response) {

  const contentType =
    response.headers.get(
      "content-type"
    ) || "";

  if (
    contentType.includes(
      "application/json"
    )
  ) {

    return await response.json();
  }

  const text =
    await response.text();

  try {

    return JSON.parse(text);

  } catch {

    return text;
  }
}


function refreshIcons() {

  if (
    window.lucide &&
    typeof window.lucide.createIcons ===
      "function"
  ) {

    window.lucide.createIcons();
  }
}


/* =========================================================
   STATUS CONFIGURATION
   ========================================================= */

const STATUS_META = {

  pending: {

    label: "Aguardando aprovação",

    icon: "clock",
  },

  confirmed: {

    label: "Aprovado",

    icon: "check-circle",
  },

  delivering: {

    label: "Saiu para entrega",

    icon: "truck",
  },

  delivered: {

    label: "Concluído",

    icon: "circle-check",
  },

  cancelled: {

    label: "Cancelado",

    icon: "x-circle",
  },
};


const STATUS_ORDER = [

  "pending",

  "confirmed",

  "delivering",

  "delivered",

  "cancelled",

];


const NEXT_ACTION = {

  pending: {

    status: "confirmed",

    label: "Aprovar",

    icon: "check",
  },

  confirmed: {

    status: "delivering",

    label: "Enviar",

    icon: "truck",
  },

  delivering: {

    status: "delivered",

    label: "Concluir",

    icon: "check-circle",
  },

  delivered: null,

  cancelled: null,
};


/* =========================================================
   ORDERS MODULE
   ========================================================= */

const OrdersModule = {

  apiBase: "",

  orders: [],

  selectedOrderId: null,

  connected: false,

  loading: false,

  autoRefreshTimer: null,

  autoRefreshInterval: 8000,


  /* ---------------------------------------------------------
     STATUS API → FRONTEND
     --------------------------------------------------------- */

  normalizeOrderStatus(status) {

    const normalized =
      String(status || "")
        .trim()
        .toUpperCase();

    const statusMap = {

      PENDING: "pending",

      WAITING: "pending",

      APPROVED: "confirmed",

      CONFIRMED: "confirmed",

      DELIVERING: "delivering",

      OUT_FOR_DELIVERY: "delivering",

      COMPLETED: "delivered",

      DELIVERED: "delivered",

      CANCELLED: "cancelled",

      CANCELED: "cancelled",
    };

    return (
      statusMap[normalized] ||
      "pending"
    );
  },


  /* ---------------------------------------------------------
     STATUS FRONTEND → API
     --------------------------------------------------------- */

  apiStatusFromFrontend(status) {

    const statusMap = {

      pending: "PENDING",

      confirmed: "APPROVED",

      delivering: "OUT_FOR_DELIVERY",

      delivered: "COMPLETED",

      cancelled: "CANCELLED",
    };

    return (
      statusMap[status] ||
      status
    );
  },


  /* ---------------------------------------------------------
     CONNECTION
     --------------------------------------------------------- */

  setConnectionStatus(connected) {

    this.connected =
      Boolean(connected);

    if (
      !DOM.connectionDot ||
      !DOM.connectionText
    ) {

      return;
    }

    if (connected) {

      DOM.connectionDot.classList.add(
        "connected"
      );

      DOM.connectionText.textContent =
        "Conectado";

    } else {

      DOM.connectionDot.classList.remove(
        "connected"
      );

      DOM.connectionText.textContent =
        "Desconectado";
    }
  },


  /* ---------------------------------------------------------
     LOADING
     --------------------------------------------------------- */

  setLoading(loading) {

    this.loading =
      Boolean(loading);

    if (
      !DOM.refreshOrdersButton
    ) {

      return;
    }

    DOM.refreshOrdersButton.disabled =
      loading;

    const icon =
      DOM.refreshOrdersButton.querySelector(
        "[data-lucide]"
      );

    if (icon) {

      icon.classList.toggle(
        "animate-spin",
        loading
      );
    }
  },


  /* ---------------------------------------------------------
     FETCH ORDERS
     --------------------------------------------------------- */

  async fetchOrders() {

    if (this.loading) {

      return;
    }

    this.setLoading(true);

    try {

      const url =
        buildApiUrl(
          API_CONFIG.orders.list
        );

      console.log(
        "[OrdersModule] Buscando pedidos:",
        url
      );

      const response =
        await fetch(
          url,
          {
            method: "GET",

            headers: {
              Accept:
                "application/json",
            },
          }
        );

      const data =
        await parseResponse(
          response
        );

      if (!response.ok) {

        throw new Error(
          `Erro ao buscar pedidos: HTTP ${response.status}`
        );
      }

      console.log(
        "[OrdersModule] Resposta da API:",
        data
      );

      let rawOrders = [];

      if (Array.isArray(data)) {

        rawOrders = data;

      } else if (
        Array.isArray(data?.orders)
      ) {

        rawOrders = data.orders;

      } else if (
        Array.isArray(data?.data)
      ) {

        rawOrders = data.data;

      } else if (
        Array.isArray(data?.data?.orders)
      ) {

        rawOrders =
          data.data.orders;
      }

      this.orders =
        rawOrders.map(
          (order) => ({

            ...order,

            status:
              this.normalizeOrderStatus(
                order.status
              ),
          })
        );

      this.setConnectionStatus(
        true
      );

      this.renderBoard();

      this.updateCount();

    } catch (error) {

      console.error(
        "[OrdersModule] Erro ao buscar pedidos:",
        error
      );

      this.setConnectionStatus(
        false
      );

    } finally {

      this.setLoading(false);

      refreshIcons();
    }
  },


  /* ---------------------------------------------------------
     FETCH ORDER DETAILS
     --------------------------------------------------------- */

  async fetchOrderDetails(
    orderId
  ) {

    try {

      const response =
        await fetch(
          buildApiUrl(
            API_CONFIG.orders.details(
              orderId
            )
          ),
          {
            method: "GET",

            headers: {
              Accept:
                "application/json",
            },
          }
        );

      const data =
        await parseResponse(
          response
        );

      if (!response.ok) {

        throw new Error(
          `Erro ao buscar detalhes: HTTP ${response.status}`
        );
      }

      return data;

    } catch (error) {

      console.error(
        "[OrdersModule] Erro ao buscar detalhes:",
        error
      );

      throw error;
    }
  },


  /* ---------------------------------------------------------
     PATCH STATUS
     --------------------------------------------------------- */

  async patchStatus(
    orderId,
    newStatus
  ) {

    const index =
      this.orders.findIndex(
        (order) =>
          String(
            order.id ??
            order.order_id ??
            order.orderId
          ) === String(orderId)
      );

    if (index === -1) {

      console.warn(
        "[OrdersModule] Pedido não encontrado:",
        orderId
      );

      return;
    }

    const previousStatus =
      this.orders[index].status;

    this.orders[index].status =
      newStatus;

    this.renderBoard();

    const apiStatus =
      this.apiStatusFromFrontend(
        newStatus
      );

    try {

      const url =
        buildApiUrl(
          API_CONFIG.orders.status(
            orderId
          )
        );

      const response =
        await fetch(
          url,
          {
            method: "PATCH",

            headers: {

              "Content-Type":
                "application/json",

              Accept:
                "application/json",
            },

            body:
              JSON.stringify({
                status: apiStatus,
              }),
          }
        );

      const data =
        await parseResponse(
          response
        );

      console.log(
        "[OrdersModule] Resposta PATCH:",
        data
      );

      if (!response.ok) {

        throw new Error(
          `Erro ao atualizar status: HTTP ${response.status}`
        );
      }

      this.setConnectionStatus(
        true
      );

      await this.fetchOrders();

    } catch (error) {

      console.error(
        "[OrdersModule] Erro ao atualizar status:",
        error
      );

      this.orders[index].status =
        previousStatus;

      this.renderBoard();

      this.setConnectionStatus(
        false
      );

      alert(
        "Não foi possível atualizar o status do pedido."
      );

    } finally {

      refreshIcons();
    }
  },


  /* ---------------------------------------------------------
     UPDATE COUNT
     --------------------------------------------------------- */

  updateCount() {

    if (!DOM.ordersCount) {

      return;
    }

    DOM.ordersCount.textContent =
      this.orders.length;
  },


  /* ---------------------------------------------------------
     RENDER BOARD
     --------------------------------------------------------- */

  renderBoard() {

    if (!DOM.ordersBoard) {

      return;
    }

    if (!this.orders.length) {

      DOM.ordersBoard.innerHTML = `

        <div class="col-span-full flex flex-col items-center justify-center py-20 text-center">

          <div class="w-14 h-14 rounded-full bg-[var(--paper-deep)] flex items-center justify-center mb-4">

            <i
              data-lucide="clipboard-list"
              class="w-6 h-6 text-[var(--muted)]"
            ></i>

          </div>

          <h3 class="font-display text-xl font-semibold">
            Nenhum pedido
          </h3>

          <p class="text-sm text-[var(--muted)] mt-2">
            Não existem pedidos para exibir no momento.
          </p>

        </div>
      `;

      refreshIcons();

      return;
    }

    DOM.ordersBoard.innerHTML =
      STATUS_ORDER
        .map(
          (status) =>
            this.renderColumn(status)
        )
        .join("");

    refreshIcons();
  },


  /* ---------------------------------------------------------
     RENDER COLUMN
     --------------------------------------------------------- */

  renderColumn(status) {

    const meta =
      STATUS_META[status] || {

        label: status,

        icon: "circle",
      };

    const orders =
      this.orders.filter(
        (order) =>
          this.normalizeOrderStatus(
            order.status
          ) === status
      );

    return `

      <section class="order-column">

        <div class="order-column-header">

          <div class="flex items-center gap-2">

            <div class="status-icon">

              <i
                data-lucide="${escapeHtml(
                  meta.icon
                )}"
                class="w-4 h-4"
              ></i>

            </div>

            <div>

              <h3 class="font-semibold text-sm">
                ${escapeHtml(
                  meta.label
                )}
              </h3>

              <p class="text-[11px] text-[var(--muted)]">

                ${orders.length}

                ${
                  orders.length === 1
                    ? "pedido"
                    : "pedidos"
                }

              </p>

            </div>

          </div>

        </div>

        <div class="order-column-body">

          ${
            orders.length
              ? orders
                  .map(
                    (order) =>
                      this.renderOrderCard(
                        order
                      )
                  )
                  .join("")
              : `

                <div class="empty-column">

                  <i
                    data-lucide="inbox"
                    class="w-5 h-5"
                  ></i>

                  <span>
                    Nenhum pedido
                  </span>

                </div>
              `
          }

        </div>

      </section>
    `;
  },


  /* ---------------------------------------------------------
     RENDER ORDER CARD
     --------------------------------------------------------- */

  renderOrderCard(order) {

    const orderId =
      order.id ??
      order.order_id ??
      order.orderId;

    const customer =
      order.customer_name ||
      order.customer ||
      order.name ||
      "Cliente";

    const phone =
      order.customer_phone ||
      order.phone ||
      order.phone_number ||
      "";

    const address =
      order.address ||
      order.delivery_address ||
      "";

    const total =
      order.total ??
      order.total_amount ??
      order.amount ??
      0;

    const createdAt =
      order.created_at ||
      order.createdAt ||
      order.date ||
      order.created;

    const status =
      this.normalizeOrderStatus(
        order.status
      );

    const meta =
      STATUS_META[status] || {

        label: status || "—",

        icon: "circle",
      };

    const nextAction =
      NEXT_ACTION[status];

    return `

      <article
        class="order-card"
        data-order-id="${escapeHtml(
          orderId
        )}"
      >

        <div class="flex items-start justify-between gap-3">

          <div class="min-w-0">

            <p class="text-[11px] uppercase tracking-wider text-[var(--muted)]">
              Pedido #${escapeHtml(
                orderId
              )}
            </p>

            <h4 class="font-semibold text-base mt-1 truncate">
              ${escapeHtml(
                customer
              )}
            </h4>

          </div>

          <span class="order-status-badge">
            ${escapeHtml(
              meta.label
            )}
          </span>

        </div>

        <div class="mt-4 pt-3 border-t border-[var(--line)]">

          <div class="flex items-center justify-between gap-3">

            <div class="flex items-center gap-2 text-xs text-[var(--muted)]">

              <i
                data-lucide="clock"
                class="w-3.5 h-3.5"
              ></i>

              <span>
                ${escapeHtml(
                  formatDate(
                    createdAt
                  )
                )}
              </span>

            </div>

            <strong class="text-sm">
              ${formatCurrency(
                total
              )}
            </strong>

          </div>

        </div>

        ${
          phone || address
            ? `

              <div class="mt-3 space-y-1">

                ${
                  phone
                    ? `

                      <div class="flex items-center gap-2 text-xs text-[var(--muted)]">

                        <i
                          data-lucide="phone"
                          class="w-3.5 h-3.5"
                        ></i>

                        <span>
                          ${escapeHtml(
                            phone
                          )}
                        </span>

                      </div>
                    `
                    : ""
                }

                ${
                  address
                    ? `

                      <div class="flex items-start gap-2 text-xs text-[var(--muted)]">

                        <i
                          data-lucide="map-pin"
                          class="w-3.5 h-3.5 mt-0.5 flex-shrink-0"
                        ></i>

                        <span class="line-clamp-2">
                          ${escapeHtml(
                            address
                          )}
                        </span>

                      </div>
                    `
                    : ""
                }

              </div>
            `
            : ""
        }

        <div class="flex gap-2 mt-4">

          <button
            type="button"
            class="btn btn-card flex-1"
            data-action="details"
            data-order-id="${escapeHtml(
              orderId
            )}"
          >

            <i
              data-lucide="eye"
              class="w-4 h-4"
            ></i>

            <span>
              Detalhes
            </span>

          </button>

          ${
            nextAction
              ? `

                <button
                  type="button"
                  class="btn btn-card-primary flex-1"
                  data-action="status"
                  data-order-id="${escapeHtml(
                    orderId
                  )}"
                  data-new-status="${escapeHtml(
                    nextAction.status
                  )}"
                >

                  <i
                    data-lucide="${escapeHtml(
                      nextAction.icon
                    )}"
                    class="w-4 h-4"
                  ></i>

                  <span>
                    ${escapeHtml(
                      nextAction.label
                    )}
                  </span>

                </button>
              `
              : ""
          }

        </div>

      </article>
    `;
  },


  /* ---------------------------------------------------------
     OPEN ORDER MODAL
     --------------------------------------------------------- */

  async openOrderModal(
    orderId
  ) {

    this.selectedOrderId =
      orderId;

    if (!DOM.orderModal) {

      return;
    }

    if (DOM.modalOrderTitle) {

      DOM.modalOrderTitle.textContent =
        `Pedido #${orderId}`;
    }

    if (DOM.modalOrderContent) {

      DOM.modalOrderContent.innerHTML = `

        <div class="flex items-center justify-center py-12">

          <i
            data-lucide="loader-circle"
            class="w-8 h-8 animate-spin"
          ></i>

          <span class="ml-3 text-sm text-[var(--muted)]">
            Carregando detalhes...
          </span>

        </div>
      `;
    }

    DOM.orderModal.classList.remove(
      "hidden"
    );

    refreshIcons();

    try {

      let order =
        this.orders.find(
          (item) =>
            String(
              item.id ??
              item.order_id ??
              item.orderId
            ) === String(orderId)
        );

      try {

        const details =
          await this.fetchOrderDetails(
            orderId
          );

        if (details) {

          const detailOrder =
            details.order ||
            details.data ||
            details;

          if (
            detailOrder &&
            typeof detailOrder ===
              "object"
          ) {

            order = {
              ...order,
              ...detailOrder,
            };
          }
        }

      } catch (detailsError) {

        console.warn(
          "[OrdersModule] Não foi possível buscar endpoint de detalhes. Usando dados da listagem.",
          detailsError
        );
      }

      if (!order) {

        throw new Error(
          `Pedido #${orderId} não encontrado.`
        );
      }

      const html =
        this.renderOrderDetails(
          order
        );

      if (DOM.modalOrderContent) {

        DOM.modalOrderContent.innerHTML =
          html;
      }

      refreshIcons();

    } catch (error) {

      console.error(
        "[OrdersModule] Erro ao carregar detalhes:",
        error
      );

      if (DOM.modalOrderContent) {

        DOM.modalOrderContent.innerHTML = `

          <div class="flex flex-col items-center justify-center py-12 text-center">

            <i
              data-lucide="circle-alert"
              class="w-10 h-10 mb-3"
            ></i>

            <p class="font-medium">
              Não foi possível carregar o pedido.
            </p>

            <p class="text-sm opacity-60 mt-1">
              ${escapeHtml(
                error.message
              )}
            </p>

          </div>
        `;
      }

      refreshIcons();
    }
  },


  /* ---------------------------------------------------------
     RENDER ORDER DETAILS
     --------------------------------------------------------- */

  renderOrderDetails(data) {

    const order =
      data?.order || data;

    const customer =
      order.customer_name ||
      order.customer ||
      order.name ||
      "—";

    const phone =
      order.phone ||
      order.customer_phone ||
      order.phone_number ||
      "—";

    const address =
      order.address ||
      order.delivery_address ||
      "—";

    const status =
      this.normalizeOrderStatus(
        order.status
      );

    const total =
      order.total ??
      order.total_amount ??
      order.amount ??
      0;

    const paymentMethod =
      order.payment_method ||
      order.paymentMethod ||
      "—";

    const cashReceived =
      order.cash_received ??
      order.cashReceived ??
      null;

    const changeDue =
      order.change_due ??
      order.changeDue ??
      null;

    const createdAt =
      order.created_at ||
      order.createdAt ||
      order.date ||
      order.created;

    const items =
      order.items ||
      order.order_items ||
      data?.items ||
      [];

    const statusMeta =
      STATUS_META[status] || {

        label: status,

        icon: "circle",
      };

    return `

      <div class="space-y-6">

        <div>

          <h3 class="details-section-title">
            Cliente
          </h3>

          <div class="details-grid">

            <div>

              <span class="details-label">
                Nome
              </span>

              <span class="details-value">
                ${escapeHtml(
                  customer
                )}
              </span>

            </div>

            <div>

              <span class="details-label">
                Telefone
              </span>

              <span class="details-value">
                ${escapeHtml(
                  phone
                )}
              </span>

            </div>

          </div>

        </div>


        <div>

          <h3 class="details-section-title">
            Entrega
          </h3>

          <div class="details-value">
            ${escapeHtml(
              address
            )}
          </div>

        </div>


        <div>

          <h3 class="details-section-title">
            Status
          </h3>

          <div class="inline-flex items-center gap-2 order-status-badge">

            <i
              data-lucide="${escapeHtml(
                statusMeta.icon
              )}"
              class="w-4 h-4"
            ></i>

            ${escapeHtml(
              statusMeta.label
            )}

          </div>

        </div>


        <div>

          <h3 class="details-section-title">
            Pagamento
          </h3>

          <div class="details-grid">

            <div>

              <span class="details-label">
                Método
              </span>

              <span class="details-value">
                ${escapeHtml(
                  String(
                    paymentMethod
                  ).toUpperCase()
                )}
              </span>

            </div>

            ${
              cashReceived !== null
                ? `

                  <div>

                    <span class="details-label">
                      Valor recebido
                    </span>

                    <span class="details-value">
                      ${formatCurrency(
                        cashReceived
                      )}
                    </span>

                  </div>
                `
                : ""
            }

            ${
              changeDue !== null
                ? `

                  <div>

                    <span class="details-label">
                      Troco
                    </span>

                    <span class="details-value">
                      ${formatCurrency(
                        changeDue
                      )}
                    </span>

                  </div>
                `
                : ""
            }

          </div>

        </div>


        ${
          createdAt
            ? `

              <div>

                <h3 class="details-section-title">
                  Pedido realizado
                </h3>

                <div class="details-value">
                  ${escapeHtml(
                    formatDate(
                      createdAt
                    )
                  )}
                </div>

              </div>
            `
            : ""
        }


        <div>

          <div class="flex items-center justify-between mb-3">

            <h3 class="details-section-title mb-0">
              Itens
            </h3>

            <span class="text-xs text-[var(--muted)]">

              ${
                Array.isArray(items)
                  ? items.length
                  : 0
              }

              ${
                Array.isArray(items) &&
                items.length === 1
                  ? "item"
                  : "itens"
              }

            </span>

          </div>


          <div class="space-y-2">

            ${
              Array.isArray(items) &&
              items.length
                ? items
                    .map(
                      (item) => {

                        const name =
                          item.name ||
                          item.product_name ||
                          item.product ||
                          item.productName ||
                          "Produto";

                        const quantity =
                          item.quantity ??
                          item.qty ??
                          1;

                        const price =
                          item.price ??
                          item.unit_price ??
                          item.unitPrice ??
                          0;

                        const subtotal =
                          item.subtotal ??
                          item.total ??
                          Number(
                            quantity
                          ) *
                          Number(
                            price
                          );

                        return `

                          <div class="flex items-center justify-between gap-4 rounded-xl border border-[var(--line)] p-3">

                            <div class="min-w-0">

                              <div class="font-medium text-sm">
                                ${escapeHtml(
                                  name
                                )}
                              </div>

                              <div class="text-xs text-[var(--muted)] mt-1">

                                ${escapeHtml(
                                  quantity
                                )}

                                ×

                                ${formatCurrency(
                                  price
                                )}

                              </div>

                            </div>

                            <strong class="text-sm whitespace-nowrap">
                              ${formatCurrency(
                                subtotal
                              )}
                            </strong>

                          </div>
                        `;
                      }
                    )
                    .join("")
                : `

                  <div class="text-sm text-[var(--muted)]">
                    Nenhum item informado.
                  </div>
                `
            }

          </div>

        </div>


        <div class="pt-5 border-t border-[var(--line)]">

          <div class="flex items-center justify-between">

            <span class="font-semibold">
              Total
            </span>

            <strong class="font-display text-2xl">
              ${formatCurrency(
                total
              )}
            </strong>

          </div>

        </div>

      </div>
    `;
  },


  /* ---------------------------------------------------------
     CLOSE MODAL
     --------------------------------------------------------- */

  closeOrderModal() {

    if (!DOM.orderModal) {

      return;
    }

    DOM.orderModal.classList.add(
      "hidden"
    );

    this.selectedOrderId =
      null;
  },


  /* ---------------------------------------------------------
     EVENTS
     --------------------------------------------------------- */

  setupEvents() {

    if (DOM.refreshOrdersButton) {

      DOM.refreshOrdersButton.addEventListener(
        "click",
        () =>
          this.fetchOrders()
      );
    }


    if (
      DOM.closeOrderModalButton
    ) {

      DOM.closeOrderModalButton.addEventListener(
        "click",
        () =>
          this.closeOrderModal()
      );
    }


    if (DOM.orderModal) {

      DOM.orderModal.addEventListener(
        "click",
        (event) => {

          if (
            event.target ===
            DOM.orderModal
          ) {

            this.closeOrderModal();
          }
        }
      );
    }


    if (DOM.ordersBoard) {

      DOM.ordersBoard.addEventListener(
        "click",
        async (event) => {

          const button =
            event.target.closest(
              "[data-action]"
            );

          if (!button) {

            return;
          }

          const action =
            button.dataset.action;

          const orderId =
            button.dataset.orderId;

          if (!orderId) {

            return;
          }

          if (
            action ===
            "details"
          ) {

            await this.openOrderModal(
              orderId
            );

            return;
          }

          if (
            action ===
            "status"
          ) {

            const newStatus =
              button.dataset.newStatus;

            if (!newStatus) {

              return;
            }

            await this.patchStatus(
              orderId,
              newStatus
            );
          }
        }
      );
    }
  },


  /* ---------------------------------------------------------
     AUTO REFRESH
     --------------------------------------------------------- */

  startAutoRefresh() {

    this.stopAutoRefresh();

    const interval =
      Number(
        this.autoRefreshInterval
      );

    if (
      !Number.isFinite(interval) ||
      interval <= 0
    ) {

      return;
    }

    this.autoRefreshTimer =
      setInterval(
        () =>
          this.fetchOrders(),
        interval
      );
  },


  stopAutoRefresh() {

    if (
      this.autoRefreshTimer
    ) {

      clearInterval(
        this.autoRefreshTimer
      );

      this.autoRefreshTimer =
        null;
    }
  },


  /* ---------------------------------------------------------
     INIT
     --------------------------------------------------------- */

  async init() {

    this.setupEvents();

    this.renderBoard();

    this.updateCount();

    await this.fetchOrders();

    this.startAutoRefresh();
  },
};


/* =========================================================
   SIMULATOR MODULE
   ========================================================= */

const SimulatorModule = {

  apiBase: "",

  endpoint:
    API_CONFIG.whatsapp.webhook,

  loading: false,

  phone: "",


  normalizePhone(value) {

    return String(value || "")
      .replace(/\D/g, "");
  },


  isValidPhone(
    phone = this.phone
  ) {

    const normalized =
      this.normalizePhone(
        phone
      );

    return (
      normalized.length === 10 ||
      normalized.length === 11
    );
  },


  getPhone() {

    return this.normalizePhone(
      DOM.simulatorPhone?.value ||
      ""
    );
  },


  updatePhoneState() {

    const phone =
      this.getPhone();

    this.phone =
      phone;

    if (
      DOM.simulatorPhoneHint
    ) {

      if (!phone) {

        DOM.simulatorPhoneHint.textContent =
          "Informe o telefone para iniciar a conversa.";

        DOM.simulatorPhoneHint.classList.remove(
          "text-[var(--rust)]"
        );

      } else if (
        this.isValidPhone(
          phone
        )
      ) {

        DOM.simulatorPhoneHint.textContent =
          "Telefone válido. Agora envie uma mensagem.";

        DOM.simulatorPhoneHint.classList.remove(
          "text-[var(--rust)]"
        );

      } else {

        DOM.simulatorPhoneHint.textContent =
          "Informe um telefone válido com DDD.";

        DOM.simulatorPhoneHint.classList.add(
          "text-[var(--rust)]"
        );
      }
    }
  },


  focusPhone() {

    setTimeout(
      () => {

        if (
          DOM.simulatorPhone
        ) {

          DOM.simulatorPhone.focus();

          DOM.simulatorPhone.select();
        }

      },
      50
    );
  },


  focusMessage() {

    setTimeout(
      () => {

        DOM.simulatorInput?.focus();

      },
      50
    );
  },


  updateEndpoint() {

    if (
      !DOM.simulatorEndpoint
    ) {

      return;
    }

    DOM.simulatorEndpoint.textContent =
      buildApiUrl(
        this.endpoint
      );
  },


  setLoading(loading) {

    this.loading =
      Boolean(loading);

    if (
      !DOM.sendSimulatorButton
    ) {

      return;
    }

    DOM.sendSimulatorButton.disabled =
      loading;

    const icon =
      DOM.sendSimulatorButton.querySelector(
        "[data-lucide]"
      );

    if (icon) {

      icon.classList.toggle(
        "animate-spin",
        loading
      );
    }
  },


  extractResponseMessage(data) {

    if (
      typeof data ===
      "string"
    ) {

      return data;
    }

    if (
      !data ||
      typeof data !==
        "object"
    ) {

      return String(
        data ?? ""
      );
    }

    const candidates = [

      data.reply_message,

      data.message,

      data.response,

      data.reply,

      data.answer,

      data.text,

      data.content,

      data.output,

      data.data?.reply_message,

      data.data?.message,

      data.data?.response,

      data.data?.reply,

      data.data?.answer,

      data.data?.text,

      data.data?.content,

      data.data?.output,

    ];

    for (
      const value of candidates
    ) {

      if (
        value !== undefined &&
        value !== null &&
        value !== ""
      ) {

        if (
          typeof value ===
          "object"
        ) {

          return JSON.stringify(
            value,
            null,
            2
          );
        }

        return String(value);
      }
    }

    return JSON.stringify(
      data,
      null,
      2
    );
  },


  addMessage(
    type,
    message
  ) {

    if (
      !DOM.simulatorMessages
    ) {

      return;
    }

    if (
      DOM.simulatorEmptyState
    ) {

      DOM.simulatorEmptyState.classList.add(
        "hidden"
      );
    }

    const wrapper =
      document.createElement(
        "div"
      );

    wrapper.className =
      `simulator-message ${
        type === "user"
          ? "simulator-message-user"
          : "simulator-message-bot"
      }`;

    wrapper.innerHTML = `

      <div class="simulator-message-bubble">

        ${escapeHtml(
          message
        ).replace(
          /\n/g,
          "<br>"
        )}

      </div>
    `;

    DOM.simulatorMessages.appendChild(
      wrapper
    );

    DOM.simulatorMessages.scrollTop =
      DOM.simulatorMessages.scrollHeight;
  },


  async sendMessage() {

    if (this.loading) {

      return;
    }

    const phone =
      this.getPhone();

    if (
      !this.isValidPhone(
        phone
      )
    ) {

      this.updatePhoneState();

      this.addMessage(
        "bot",
        "Informe um número de telefone válido antes de enviar a mensagem."
      );

      this.focusPhone();

      return;
    }

    this.phone =
      phone;

    const message =
      DOM.simulatorInput?.value?.trim();

    if (!message) {

      this.focusMessage();

      return;
    }

    const requestPayload = {

      phone:
        this.phone,

      message:
        message,
    };

    this.addMessage(
      "user",
      message
    );

    if (
      DOM.simulatorInput
    ) {

      DOM.simulatorInput.value =
        "";
    }

    this.updateDebugRequest(
      requestPayload
    );

    this.setLoading(
      true
    );

    try {

      const response =
        await fetch(
          buildApiUrl(
            this.endpoint
          ),
          {
            method: "POST",

            headers: {

              "Content-Type":
                "application/json",

              Accept:
                "application/json",
            },

            body:
              JSON.stringify(
                requestPayload
              ),
          }
        );

      const data =
        await parseResponse(
          response
        );

      this.updateDebugResponse(
        response,
        data
      );

      if (!response.ok) {

        const detail =
          typeof data ===
            "object" &&
          data !== null
            ? (
                data.detail ||
                data.message ||
                data.error
              )
            : data;

        throw new Error(
          detail
            ? String(detail)
            : `HTTP ${response.status}`
        );
      }

      const messageResponse =
        this.extractResponseMessage(
          data
        );

      this.addMessage(
        "bot",
        messageResponse
      );

    } catch (error) {

      console.error(
        "[SimulatorModule] Erro:",
        error
      );

      const errorMessage =
        error?.message ||
        "Erro ao processar a mensagem.";

      this.addMessage(
        "bot",
        `Erro: ${errorMessage}`
      );

      if (
        DOM.simulatorHttpStatus
      ) {

        DOM.simulatorHttpStatus.textContent =
          "ERRO";
      }

      if (
        DOM.simulatorResponse
      ) {

        DOM.simulatorResponse.textContent =
          errorMessage;
      }

    } finally {

      this.setLoading(
        false
      );

      this.focusMessage();

      refreshIcons();
    }
  },


  updateDebugRequest(
    payload
  ) {

    if (
      !DOM.simulatorRequest
    ) {

      return;
    }

    DOM.simulatorRequest.textContent =
      JSON.stringify(
        payload,
        null,
        2
      );
  },


  updateDebugResponse(
    response,
    data
  ) {

    if (
      DOM.simulatorHttpStatus
    ) {

      DOM.simulatorHttpStatus.textContent =
        `${response.status} ${response.statusText}`;
    }

    if (
      DOM.simulatorResponse
    ) {

      DOM.simulatorResponse.textContent =
        typeof data ===
        "string"

          ? data

          : JSON.stringify(
              data,
              null,
              2
            );
    }
  },


  clear() {

    if (
      DOM.simulatorMessages
    ) {

      DOM.simulatorMessages.innerHTML =
        "";
    }

    if (
      DOM.simulatorEmptyState &&
      DOM.simulatorMessages
    ) {

      DOM.simulatorMessages.appendChild(
        DOM.simulatorEmptyState
      );

      DOM.simulatorEmptyState.classList.remove(
        "hidden"
      );
    }

    if (
      DOM.simulatorRequest
    ) {

      DOM.simulatorRequest.textContent =
        "—";
    }

    if (
      DOM.simulatorResponse
    ) {

      DOM.simulatorResponse.textContent =
        "—";
    }

    if (
      DOM.simulatorHttpStatus
    ) {

      DOM.simulatorHttpStatus.textContent =
        "—";
    }

    this.phone =
      "";

    if (
      DOM.simulatorPhone
    ) {

      DOM.simulatorPhone.value =
        "";
    }

    if (
      DOM.simulatorInput
    ) {

      DOM.simulatorInput.value =
        "";
    }

    this.updatePhoneState();

    this.focusPhone();

    refreshIcons();
  },


  setupEvents() {

    if (
      DOM.sendSimulatorButton
    ) {

      DOM.sendSimulatorButton.addEventListener(
        "click",
        () =>
          this.sendMessage()
      );
    }

    if (
      DOM.clearSimulatorButton
    ) {

      DOM.clearSimulatorButton.addEventListener(
        "click",
        () =>
          this.clear()
      );
    }

    if (
      DOM.simulatorPhone
    ) {

      DOM.simulatorPhone.addEventListener(
        "input",
        () => {

          this.updatePhoneState();

          const phone =
            this.getPhone();

          if (
            this.isValidPhone(
              phone
            )
          ) {

            this.phone =
              phone;
          }
        }
      );

      DOM.simulatorPhone.addEventListener(
        "keydown",
        (event) => {

          if (
            event.key ===
            "Enter"
          ) {

            event.preventDefault();

            if (
              this.isValidPhone(
                this.getPhone()
              )
            ) {

              this.focusMessage();
            }
          }
        }
      );
    }

    if (
      DOM.simulatorInput
    ) {

      DOM.simulatorInput.addEventListener(
        "keydown",
        (event) => {

          if (
            event.key ===
              "Enter" &&
            !event.shiftKey
          ) {

            event.preventDefault();

            this.sendMessage();
          }
        }
      );
    }
  },


  init() {

    this.apiBase =
      OrdersModule.apiBase;

    this.setupEvents();

    this.updateEndpoint();

    this.updatePhoneState();
  },
};


/* =========================================================
   ADMIN MODULE
   ========================================================= */

const AdminModule = {

  loading: false,

  initialized: false,

  data: null,


  pad(value) {

    return String(
      value
    ).padStart(
      2,
      "0"
    );
  },


  formatInputDate(
    date
  ) {

    const year =
      date.getFullYear();

    const month =
      this.pad(
        date.getMonth() + 1
      );

    const day =
      this.pad(
        date.getDate()
      );

    return `${year}-${month}-${day}`;
  },


  parseInputDate(
    value
  ) {

    if (!value) {

      return null;
    }

    const parts =
      String(value)
        .split("-")
        .map(Number);

    if (
      parts.length !== 3
    ) {

      return null;
    }

    const [
      year,
      month,
      day,
    ] = parts;

    if (
      !year ||
      !month ||
      !day
    ) {

      return null;
    }

    return new Date(
      year,
      month - 1,
      day
    );
  },


  getToday() {

    const today =
      new Date();

    today.setHours(
      0,
      0,
      0,
      0
    );

    return today;
  },


  getDaysAgo(
    days
  ) {

    const date =
      this.getToday();

    date.setDate(
      date.getDate() -
      Number(days)
    );

    return date;
  },


  setDateRange(
    startDate,
    endDate
  ) {

    if (
      DOM.adminStartDate
    ) {

      DOM.adminStartDate.value =
        this.formatInputDate(
          startDate
        );
    }

    if (
      DOM.adminEndDate
    ) {

      DOM.adminEndDate.value =
        this.formatInputDate(
          endDate
        );
    }

    this.updatePeriodLabel();
  },


  setDefaultDateRange() {

    this.setDateRange(
      this.getDaysAgo(6),
      this.getToday()
    );
  },


  getDateRange() {

    return {

      start:
        this.parseInputDate(
          DOM.adminStartDate?.value
        ),

      end:
        this.parseInputDate(
          DOM.adminEndDate?.value
        ),

      startValue:
        DOM.adminStartDate?.value ||
        "",

      endValue:
        DOM.adminEndDate?.value ||
        "",
    };
  },


  validateDateRange() {

    const range =
      this.getDateRange();

    if (
      !range.start ||
      !range.end
    ) {

      throw new Error(
        "Informe a data inicial e a data final."
      );
    }

    if (
      range.start >
      range.end
    ) {

      throw new Error(
        "A data inicial não pode ser maior que a data final."
      );
    }

    return range;
  },


  formatDisplayDate(
    value
  ) {

    const date =
      this.parseInputDate(
        value
      );

    if (!date) {

      return "—";
    }

    return new Intl.DateTimeFormat(
      "pt-BR"
    ).format(date);
  },


  updatePeriodLabel() {

    if (
      !DOM.adminPeriodLabel
    ) {

      return;
    }

    const range =
      this.getDateRange();

    if (
      !range.startValue ||
      !range.endValue
    ) {

      DOM.adminPeriodLabel.textContent =
        "Período não definido";

      return;
    }

    DOM.adminPeriodLabel.textContent =
      `${this.formatDisplayDate(
        range.startValue
      )} até ${this.formatDisplayDate(
        range.endValue
      )}`;
  },


  setLoading(
    loading
  ) {

    this.loading =
      Boolean(loading);

    if (
      DOM.adminLoading
    ) {

      DOM.adminLoading.classList.toggle(
        "hidden",
        !loading
      );
    }

    if (
      DOM.refreshAdminButton
    ) {

      DOM.refreshAdminButton.disabled =
        loading;
    }
  },


  showError(
    message
  ) {

    if (
      DOM.adminErrorMessage
    ) {

      DOM.adminErrorMessage.textContent =
        message;
    }

    if (
      DOM.adminError
    ) {

      DOM.adminError.classList.remove(
        "hidden"
      );
    }
  },


  hideError() {

    if (
      DOM.adminError
    ) {

      DOM.adminError.classList.add(
        "hidden"
      );
    }
  },


  getNumber(
    ...values
  ) {

    for (
      const value of values
    ) {

      if (
        value !== undefined &&
        value !== null &&
        value !== ""
      ) {

        const number =
          Number(value);

        if (
          Number.isFinite(
            number
          )
        ) {

          return number;
        }
      }
    }

    return 0;
  },


  getPayload(
    data
  ) {

    if (
      !data ||
      typeof data !==
        "object"
    ) {

      return {};
    }

    if (
      data.summary ||
      data.top_products
    ) {

      return data;
    }

    if (
      data.data &&
      typeof data.data ===
        "object"
    ) {

      return data.data;
    }

    if (
      data.dashboard &&
      typeof data.dashboard ===
        "object"
    ) {

      return data.dashboard;
    }

    if (
      data.result &&
      typeof data.result ===
        "object"
    ) {

      return data.result;
    }

    return data;
  },


  normalizeProduct(
    product
  ) {

    if (
      !product ||
      typeof product !==
        "object"
    ) {

      return {

        name: "Produto",

        category: "—",

        volume: "—",

        quantity: 0,

        revenue: 0,
      };
    }

    const name =
      product.product_name ??
      product.productName ??
      product.name ??
      product.product ??
      "Produto";

    const category =
      product.category ??
      product.product_category ??
      product.productCategory ??
      "—";

    const volume =
      product.volume ??
      product.product_volume ??
      product.productVolume ??
      "—";

    const quantity =
      this.getNumber(

        product.total_quantity_sold,

        product.totalQuantitySold,

        product.quantity,

        product.qty,

        product.units_sold,

        product.unitsSold,

        product.total_quantity,

        product.totalQuantity,

        product.count
      );

    const revenue =
      this.getNumber(

        product.total_revenue_generated,

        product.totalRevenueGenerated,

        product.revenue,

        product.total_revenue,

        product.totalRevenue,

        product.sales,

        product.total_sales,

        product.totalSales,

        product.amount
      );

    return {

      name:
        String(name),

      category:
        String(category),

      volume:
        String(volume),

      quantity,

      revenue,
    };
  },


  normalizeDashboard(
    data
  ) {

    const payload =
      this.getPayload(
        data
      );

    const summary =
      payload?.summary || {};

    const rawProducts =
      Array.isArray(
        payload?.top_products
      )

        ? payload.top_products

        : Array.isArray(
            payload?.topProducts
          )

          ? payload.topProducts

          : Array.isArray(
              payload?.products
            )

            ? payload.products

            : [];

    const products =
      rawProducts.map(
        (product) =>
          this.normalizeProduct(
            product
          )
      );

    return {

      summary: {

        total_orders:
          this.getNumber(
            summary.total_orders,
            summary.totalOrders,
            payload.total_orders,
            payload.totalOrders
          ),

        total_revenue:
          this.getNumber(
            summary.total_revenue,
            summary.totalRevenue,
            payload.total_revenue,
            payload.totalRevenue
          ),

        average_ticket:
          this.getNumber(
            summary.average_ticket,
            summary.averageTicket,
            payload.average_ticket,
            payload.averageTicket
          ),
      },

      top_products:
        products,
    };
  },


  async fetchDashboard() {

    if (this.loading) {

      return;
    }

    let range;

    try {

      range =
        this.validateDateRange();

    } catch (error) {

      this.showError(
        error.message
      );

      return;
    }

    this.setLoading(
      true
    );

    this.hideError();

    try {

      const params =
        new URLSearchParams({

          start_date:
            range.startValue,

          end_date:
            range.endValue,
        });

      const url =
        `${buildApiUrl(
          API_CONFIG.admin.dashboard
        )}?${params.toString()}`;

      console.log(
        "[AdminModule] Buscando dashboard:",
        url
      );

      const response =
        await fetch(
          url,
          {
            method: "GET",

            headers: {

              Accept:
                "application/json",
            },
          }
        );

      const data =
        await parseResponse(
          response
        );

      console.log(
        "[AdminModule] Resposta:",
        data
      );

      if (!response.ok) {

        const detail =
          typeof data ===
              "object" &&
          data !== null

            ? (
                data.detail ||
                data.message ||
                data.error
              )

            : data;

        throw new Error(

          detail

            ? String(detail)

            : `Erro ao carregar indicadores: HTTP ${response.status}`
        );
      }

      this.data =
        data;

      this.render(
        data
      );

      OrdersModule.setConnectionStatus(
        true
      );

    } catch (error) {

      console.error(
        "[AdminModule] Erro:",
        error
      );

      this.showError(
        error?.message ||
        "Não foi possível carregar os indicadores."
      );

      OrdersModule.setConnectionStatus(
        false
      );

    } finally {

      this.setLoading(
        false
      );

      refreshIcons();
    }
  },


  render(
    data
  ) {

    const dashboard =
      this.normalizeDashboard(
        data
      );

    const summary =
      dashboard.summary;

    const products =
      dashboard.top_products;


    if (
      DOM.adminTotalOrders
    ) {

      DOM.adminTotalOrders.textContent =
        summary.total_orders.toLocaleString(
          "pt-BR"
        );
    }


    if (
      DOM.adminTotalRevenue
    ) {

      DOM.adminTotalRevenue.textContent =
        formatCurrency(
          summary.total_revenue
        );
    }


    if (
      DOM.adminAverageTicket
    ) {

      DOM.adminAverageTicket.textContent =
        formatCurrency(
          summary.average_ticket
        );
    }


    if (
      DOM.adminTopProductsCount
    ) {

      DOM.adminTopProductsCount.textContent =
        products.length.toLocaleString(
          "pt-BR"
        );
    }


    this.renderProductsTable(
      products
    );

    this.renderProductsMobile(
      products
    );

    this.renderQuantityChart(
      products
    );

    this.renderRevenueChart(
      products
    );


    if (
      DOM.adminDashboardContent
    ) {

      DOM.adminDashboardContent.classList.remove(
        "hidden"
      );
    }


    if (
      DOM.adminLastUpdate
    ) {

      DOM.adminLastUpdate.textContent =
        `Atualizado em ${formatDate(
          new Date()
        )}`;
    }

    refreshIcons();
  },


  renderProductsTable(
    products
  ) {

    if (
      !DOM.adminProductsTableBody
    ) {

      return;
    }

    if (
      !products ||
      !products.length
    ) {

      DOM.adminProductsTableBody.innerHTML = `

        <tr>

          <td
            colspan="5"
            class="px-4 py-8 text-center text-sm text-[var(--muted)]"
          >

            Nenhum produto encontrado
            no período.

          </td>

        </tr>
      `;

      return;
    }

    DOM.adminProductsTableBody.innerHTML =
      products
        .map(
          (product) => `

            <tr
              class="border-t border-[var(--line)]"
            >

              <td class="px-4 py-3">

                ${escapeHtml(
                  product.name
                )}

              </td>

              <td class="px-4 py-3">

                ${escapeHtml(
                  product.category
                )}

              </td>

              <td class="px-4 py-3">

                ${escapeHtml(
                  product.volume
                )}

              </td>

              <td class="px-4 py-3">

                ${product.quantity.toLocaleString(
                  "pt-BR"
                )}

              </td>

              <td class="px-4 py-3">

                ${formatCurrency(
                  product.revenue
                )}

              </td>

            </tr>
          `
        )
        .join("");
  },


  renderProductsMobile(
    products
  ) {

    if (
      !DOM.adminProductsMobile
    ) {

      return;
    }

    if (
      !products ||
      !products.length
    ) {

      DOM.adminProductsMobile.innerHTML = `

        <div class="text-sm text-[var(--muted)]">

          Nenhum produto encontrado
          no período.

        </div>
      `;

      return;
    }

    DOM.adminProductsMobile.innerHTML =
      products
        .map(
          (product) => `

            <div
              class="rounded-xl border border-[var(--line)] p-4"
            >

              <div
                class="flex items-start justify-between gap-3"
              >

                <div class="min-w-0">

                  <div class="font-semibold truncate">

                    ${escapeHtml(
                      product.name
                    )}

                  </div>

                  <div
                    class="text-xs text-[var(--muted)] mt-1"
                  >

                    ${escapeHtml(
                      product.category
                    )}

                    ·

                    ${escapeHtml(
                      product.volume
                    )}

                  </div>

                </div>

                <strong class="whitespace-nowrap">

                  ${formatCurrency(
                    product.revenue
                  )}

                </strong>

              </div>

              <div
                class="text-sm text-[var(--muted)] mt-3"
              >

                Quantidade vendida:

                <strong class="text-[var(--foreground)]">

                  ${product.quantity.toLocaleString(
                    "pt-BR"
                  )}

                </strong>

              </div>

            </div>
          `
        )
        .join("");
  },


  renderProducts(
    products
  ) {

    const normalized =
      (products || []).map(
        (product) =>
          this.normalizeProduct(
            product
          )
      );

    this.renderProductsTable(
      normalized
    );

    this.renderProductsMobile(
      normalized
    );
  },


  renderQuantityChart(
    products
  ) {

    if (
      !DOM.adminQuantityChart
    ) {

      return;
    }

    if (
      !products ||
      !products.length
    ) {

      DOM.adminQuantityChart.innerHTML = `

        <div class="text-sm text-[var(--muted)]">

          Sem dados para exibir.

        </div>
      `;

      return;
    }

    const chartProducts =
      products.slice(
        0,
        10
      );

    const max =
      Math.max(
        ...chartProducts.map(
          (product) =>
            Number(
              product.quantity
            ) || 0
        ),
        1
      );

    DOM.adminQuantityChart.innerHTML =
      chartProducts
        .map(
          (product) => {

            const quantity =
              Number(
                product.quantity
              ) || 0;

            const percentage =
              Math.min(
                100,
                Math.max(
                  4,
                  (
                    quantity /
                    max
                  ) * 100
                )
              );

            return `

              <div class="mb-3">

                <div
                  class="flex items-center justify-between gap-3 mb-1"
                >

                  <span
                    class="text-xs truncate"
                  >

                    ${escapeHtml(
                      `${product.name} - ${product.volume}`
                    )}

                  </span>

                  <span
                    class="text-xs text-[var(--muted)]"
                  >

                    ${quantity.toLocaleString(
                      "pt-BR"
                    )}

                  </span>

                </div>

                <div
                  class="h-2 rounded-full bg-[var(--paper-deep)] overflow-hidden"
                >

                  <div
                    class="h-full rounded-full bg-[var(--rust)]"
                    style="width:${percentage}%"
                  ></div>

                </div>

              </div>
            `;
          }
        )
        .join("");
  },


  renderRevenueChart(
    products
  ) {

    if (
      !DOM.adminRevenueChart
    ) {

      return;
    }

    if (
      !products ||
      !products.length
    ) {

      DOM.adminRevenueChart.innerHTML = `

        <div class="text-sm text-[var(--muted)]">

          Sem dados para exibir.

        </div>
      `;

      return;
    }

    const chartProducts =
      products.slice(
        0,
        10
      );

    const max =
      Math.max(
        ...chartProducts.map(
          (product) =>
            Number(
              product.revenue
            ) || 0
        ),
        1
      );

    DOM.adminRevenueChart.innerHTML =
      chartProducts
        .map(
          (product) => {

            const revenue =
              Number(
                product.revenue
              ) || 0;

            const percentage =
              Math.min(
                100,
                Math.max(
                  4,
                  (
                    revenue /
                    max
                  ) * 100
                )
              );

            return `

              <div class="mb-3">

                <div
                  class="flex items-center justify-between gap-3 mb-1"
                >

                  <span
                    class="text-xs truncate"
                  >

                    ${escapeHtml(
                      `${product.name} - ${product.volume}`
                    )}

                  </span>

                  <span
                    class="text-xs text-[var(--muted)]"
                  >

                    ${formatCurrency(
                      revenue
                    )}

                  </span>

                </div>

                <div
                  class="h-2 rounded-full bg-[var(--paper-deep)] overflow-hidden"
                >

                  <div
                    class="h-full rounded-full bg-[var(--rust)]"
                    style="width:${percentage}%"
                  ></div>

                </div>

              </div>
            `;
          }
        )
        .join("");
  },


  setupEvents() {

    if (
      DOM.refreshAdminButton
    ) {

      DOM.refreshAdminButton.addEventListener(
        "click",
        () =>
          this.fetchDashboard()
      );
    }


    if (
      DOM.adminStartDate
    ) {

      DOM.adminStartDate.addEventListener(
        "change",
        () =>
          this.updatePeriodLabel()
      );
    }


    if (
      DOM.adminEndDate
    ) {

      DOM.adminEndDate.addEventListener(
        "change",
        () =>
          this.updatePeriodLabel()
      );
    }


    if (
      DOM.adminTodayButton
    ) {

      DOM.adminTodayButton.addEventListener(
        "click",
        () => {

          this.setDateRange(
            this.getToday(),
            this.getToday()
          );

          this.fetchDashboard();
        }
      );
    }


    if (
      DOM.adminSevenDaysButton
    ) {

      DOM.adminSevenDaysButton.addEventListener(
        "click",
        () => {

          this.setDateRange(
            this.getDaysAgo(6),
            this.getToday()
          );

          this.fetchDashboard();
        }
      );
    }


    if (
      DOM.adminThirtyDaysButton
    ) {

      DOM.adminThirtyDaysButton.addEventListener(
        "click",
        () => {

          this.setDateRange(
            this.getDaysAgo(29),
            this.getToday()
          );

          this.fetchDashboard();
        }
      );
    }
  },


  init() {

    if (
      this.initialized
    ) {

      return;
    }

    this.setDefaultDateRange();

    this.setupEvents();

    this.updatePeriodLabel();

    this.initialized =
      true;
  },
};


/* =========================================================
   MESSAGES MODULE
   ========================================================= */

const MessagesModule = {

  initialized: false,

  loading: false,

  messages: [],


  /* ---------------------------------------------------------
     DATE HELPERS
     --------------------------------------------------------- */

  pad(value) {

    return String(
      value
    ).padStart(
      2,
      "0"
    );
  },


  formatInputDate(
    date
  ) {

    const year =
      date.getFullYear();

    const month =
      this.pad(
        date.getMonth() + 1
      );

    const day =
      this.pad(
        date.getDate()
      );

    return `${year}-${month}-${day}`;
  },


  parseInputDate(
    value
  ) {

    if (!value) {

      return null;
    }

    const parts =
      String(value)
        .split("-")
        .map(Number);

    if (
      parts.length !== 3
    ) {

      return null;
    }

    const [
      year,
      month,
      day,
    ] = parts;

    if (
      !year ||
      !month ||
      !day
    ) {

      return null;
    }

    return new Date(
      year,
      month - 1,
      day
    );
  },


  getToday() {

    const today =
      new Date();

    today.setHours(
      0,
      0,
      0,
      0
    );

    return today;
  },


  getDaysAgo(
    days
  ) {

    const date =
      this.getToday();

    date.setDate(
      date.getDate() -
      Number(days)
    );

    return date;
  },


  setDefaultDateRange() {

    if (
      DOM.messagesStartDate
    ) {

      DOM.messagesStartDate.value =
        this.formatInputDate(
          this.getDaysAgo(6)
        );
    }

    if (
      DOM.messagesEndDate
    ) {

      DOM.messagesEndDate.value =
        this.formatInputDate(
          this.getToday()
        );
    }

    if (
      DOM.messagesLimit &&
      !DOM.messagesLimit.value
    ) {

      DOM.messagesLimit.value =
        "100";
    }
  },


  getDateRange() {

    return {

      start:
        this.parseInputDate(
          DOM.messagesStartDate?.value
        ),

      end:
        this.parseInputDate(
          DOM.messagesEndDate?.value
        ),

      startValue:
        DOM.messagesStartDate?.value ||
        "",

      endValue:
        DOM.messagesEndDate?.value ||
        "",
    };
  },


  validateDateRange() {

    const range =
      this.getDateRange();

    if (
      !range.start ||
      !range.end
    ) {

      throw new Error(
        "Informe a data inicial e a data final."
      );
    }

    if (
      range.start >
      range.end
    ) {

      throw new Error(
        "A data inicial não pode ser maior que a data final."
      );
    }

    return range;
  },


  getLimit() {

    const value =
      Number(
        DOM.messagesLimit?.value ||
        100
      );

    if (
      !Number.isFinite(value) ||
      value <= 0
    ) {

      return 100;
    }

    return Math.min(
      Math.floor(value),
      1000
    );
  },


  /* ---------------------------------------------------------
     LOADING
     --------------------------------------------------------- */

  setLoading(
    loading
  ) {

    this.loading =
      Boolean(loading);

    if (
      DOM.messagesLoading
    ) {

      DOM.messagesLoading.classList.toggle(
        "hidden",
        !loading
      );
    }

    if (
      DOM.refreshMessagesButton
    ) {

      DOM.refreshMessagesButton.disabled =
        loading;
    }
  },


  /* ---------------------------------------------------------
     ERROR
     --------------------------------------------------------- */

  showError(
    message
  ) {

    if (
      DOM.messagesErrorMessage
    ) {

      DOM.messagesErrorMessage.textContent =
        message;
    }

    if (
      DOM.messagesError
    ) {

      DOM.messagesError.classList.remove(
        "hidden"
      );
    }
  },


  hideError() {

    if (
      DOM.messagesError
    ) {

      DOM.messagesError.classList.add(
        "hidden"
      );
    }
  },


  /* ---------------------------------------------------------
     NORMALIZE RESPONSE
     --------------------------------------------------------- */

  normalizeResponse(
    data
  ) {

    if (
      Array.isArray(data)
    ) {

      return data;
    }

    if (
      Array.isArray(
        data?.messages
      )
    ) {

      return data.messages;
    }

    if (
      Array.isArray(
        data?.data
      )
    ) {

      return data.data;
    }

    if (
      Array.isArray(
        data?.data?.messages
      )
    ) {

      return data.data.messages;
    }

    return [];
  },


  /* ---------------------------------------------------------
     FETCH MESSAGES
     --------------------------------------------------------- */

  async fetchMessages() {

    if (this.loading) {

      return;
    }

    let range;

    try {

      range =
        this.validateDateRange();

    } catch (error) {

      this.showError(
        error.message
      );

      return;
    }

    this.setLoading(
      true
    );

    this.hideError();

    try {

      const params =
        new URLSearchParams({

          start_date:
            range.startValue,

          end_date:
            range.endValue,

          limit:
            String(
              this.getLimit()
            ),
        });

      const url =
        `${buildApiUrl(
          API_CONFIG.messages.list
        )}?${params.toString()}`;

      console.log(
        "[MessagesModule] Buscando mensagens:",
        url
      );

      const response =
        await fetch(
          url,
          {
            method: "GET",

            headers: {

              Accept:
                "application/json",
            },
          }
        );

      const data =
        await parseResponse(
          response
        );

      console.log(
        "[MessagesModule] Resposta:",
        data
      );

      if (!response.ok) {

        const detail =
          typeof data ===
              "object" &&
          data !== null

            ? (
                data.detail ||
                data.message ||
                data.error
              )

            : data;

        throw new Error(

          detail

            ? String(detail)

            : `Erro ao carregar mensagens: HTTP ${response.status}`
        );
      }

      this.messages =
        this.normalizeResponse(
          data
        );

      this.render();

      OrdersModule.setConnectionStatus(
        true
      );

    } catch (error) {

      console.error(
        "[MessagesModule] Erro:",
        error
      );

      this.showError(
        error?.message ||
        "Não foi possível carregar as mensagens."
      );

      OrdersModule.setConnectionStatus(
        false
      );

    } finally {

      this.setLoading(
        false
      );

      refreshIcons();
    }
  },


  /* ---------------------------------------------------------
     RENDER
     --------------------------------------------------------- */

  render() {

    if (
      !DOM.messagesTableBody
    ) {

      return;
    }

    if (
      !this.messages.length
    ) {

      DOM.messagesTableBody.innerHTML =
        "";

      if (
        DOM.messagesEmpty
      ) {

        DOM.messagesEmpty.classList.remove(
          "hidden"
        );
      }

      return;
    }

    if (
      DOM.messagesEmpty
    ) {

      DOM.messagesEmpty.classList.add(
        "hidden"
      );
    }

    DOM.messagesTableBody.innerHTML =
      this.messages
        .map(
          (item, index) => {

            const orderId =
              item?.order_id ??
              item?.orderId ??
              item?.id ??
              "—";

            const phone =
              item?.customer_phone ??
              item?.phone ??
              item?.phone_number ??
              "—";

            const messages =
              Array.isArray(
                item?.messages
              )
                ? item.messages
                : [];

            return `

              <tr
                class="border-t border-[var(--line)] hover:bg-[var(--paper-deep)] transition cursor-pointer"
                data-message-index="${index}"
              >

                <td class="px-4 py-3 font-medium">

                  #${escapeHtml(
                    orderId
                  )}

                </td>

                <td class="px-4 py-3 text-sm">

                  ${escapeHtml(
                    phone
                  )}

                </td>

                <td class="px-4 py-3 text-sm">

                  ${messages.length}

                  ${
                    messages.length === 1
                      ? "mensagem"
                      : "mensagens"
                  }

                </td>

                <td class="px-4 py-3 text-right">

                  <button
                    type="button"
                    class="btn btn-card"
                    data-message-index="${index}"
                  >

                    <i
                      data-lucide="message-square"
                      class="w-4 h-4"
                    ></i>

                    <span>
                      Ver conversa
                    </span>

                  </button>

                </td>

              </tr>
            `;
          }
        )
        .join("");

    refreshIcons();
  },


  /* ---------------------------------------------------------
     OPEN CONVERSATION
     --------------------------------------------------------- */

  openConversation(
    index
  ) {

    const item =
      this.messages[index];

    if (!item) {

      return;
    }

    if (
      !DOM.conversationModal
    ) {

      return;
    }

    const orderId =
      item?.order_id ??
      item?.orderId ??
      item?.id ??
      "—";

    const phone =
      item?.customer_phone ??
      item?.phone ??
      item?.phone_number ??
      "—";

    const messages =
      Array.isArray(
        item?.messages
      )
        ? item.messages
        : [];

    if (
      DOM.conversationModalTitle
    ) {

      DOM.conversationModalTitle.textContent =
        `Pedido #${orderId} · ${phone}`;
    }

    if (
      DOM.conversationModalContent
    ) {

      if (!messages.length) {

        DOM.conversationModalContent.innerHTML = `

          <div class="flex flex-col items-center justify-center py-12 text-center">

            <i
              data-lucide="message-square-off"
              class="w-10 h-10 mb-3 opacity-50"
            ></i>

            <p class="font-medium">
              Nenhuma mensagem encontrada.
            </p>

          </div>
        `;

      } else {

        DOM.conversationModalContent.innerHTML = `

          <div class="space-y-4">

            ${messages
              .map(
                (message) => {

                  const isUser =
                    message &&
                    Object.prototype.hasOwnProperty.call(
                      message,
                      "user"
                    );

                  const isBot =
                    message &&
                    Object.prototype.hasOwnProperty.call(
                      message,
                      "bot"
                    );

                  const text =
                    isUser
                      ? message.user
                      : isBot
                        ? message.bot
                        : (
                            message?.message ??
                            message?.text ??
                            JSON.stringify(
                              message
                            )
                          );

                  const label =
                    isUser
                      ? "Cliente"
                      : "Bot";

                  const alignment =
                    isUser
                      ? "justify-end"
                      : "justify-start";

                  const bubbleClass =
                    isUser
                      ? "bg-[var(--rust)] text-white"
                      : "bg-[var(--paper-deep)]";

                  return `

                    <div
                      class="flex ${alignment}"
                    >

                      <div
                        class="max-w-[85%]"
                      >

                        <div
                          class="text-[11px] uppercase tracking-wider text-[var(--muted)] mb-1 ${
                            isUser
                              ? "text-right"
                              : "text-left"
                          }"
                        >

                          ${escapeHtml(
                            label
                          )}

                        </div>

                        <div
                          class="rounded-2xl px-4 py-3 text-sm ${bubbleClass}"
                          style="white-space: pre-wrap;"
                        >

                          ${escapeHtml(
                            text
                          )}

                        </div>

                      </div>

                    </div>
                  `;
                }
              )
              .join("")}

          </div>
        `;
      }
    }

    DOM.conversationModal.classList.remove(
      "hidden"
    );

    refreshIcons();
  },


  /* ---------------------------------------------------------
     CLOSE CONVERSATION
     --------------------------------------------------------- */

  closeConversation() {

    if (
      !DOM.conversationModal
    ) {

      return;
    }

    DOM.conversationModal.classList.add(
      "hidden"
    );
  },


  /* ---------------------------------------------------------
     EVENTS
     --------------------------------------------------------- */

  setupEvents() {

    if (
      DOM.refreshMessagesButton
    ) {

      DOM.refreshMessagesButton.addEventListener(
        "click",
        () =>
          this.fetchMessages()
      );
    }


    if (
      DOM.messagesStartDate
    ) {

      DOM.messagesStartDate.addEventListener(
        "change",
        () =>
          this.fetchMessages()
      );
    }


    if (
      DOM.messagesEndDate
    ) {

      DOM.messagesEndDate.addEventListener(
        "change",
        () =>
          this.fetchMessages()
      );
    }


    if (
      DOM.messagesLimit
    ) {

      DOM.messagesLimit.addEventListener(
        "change",
        () =>
          this.fetchMessages()
      );
    }


    if (
      DOM.messagesTableBody
    ) {

      DOM.messagesTableBody.addEventListener(
        "click",
        (event) => {

          const target =
            event.target.closest(
              "[data-message-index]"
            );

          if (!target) {

            return;
          }

          const index =
            Number(
              target.dataset.messageIndex
            );

          if (
            !Number.isInteger(
              index
            )
          ) {

            return;
          }

          this.openConversation(
            index
          );
        }
      );
    }


    if (
      DOM.closeConversationModalButton
    ) {

      DOM.closeConversationModalButton.addEventListener(
        "click",
        () =>
          this.closeConversation()
      );
    }


    if (
      DOM.conversationModal
    ) {

      DOM.conversationModal.addEventListener(
        "click",
        (event) => {

          if (
            event.target ===
            DOM.conversationModal
          ) {

            this.closeConversation();
          }
        }
      );
    }
  },


  /* ---------------------------------------------------------
     INIT
     --------------------------------------------------------- */

  init() {

    if (
      this.initialized
    ) {

      return;
    }

    this.setDefaultDateRange();

    this.setupEvents();

    this.initialized =
      true;
  },
};


/* =========================================================
   TABS MODULE
   ========================================================= */

const TabsModule = {

  currentTab:
    "orders",


  /* ---------------------------------------------------------
     ACTIVATE
     --------------------------------------------------------- */

  activate(
    tab
  ) {

    this.currentTab =
      tab;

    const isOrders =
      tab === "orders";

    const isSimulator =
      tab === "simulator";

    const isAdmin =
      tab === "admin";

    const isMessages =
      tab === "messages";


    /* -------------------------------------------------------
       VIEWS
       ------------------------------------------------------- */

    if (
      DOM.ordersView
    ) {

      DOM.ordersView.classList.toggle(
        "hidden",
        !isOrders
      );
    }

    if (
      DOM.simulatorView
    ) {

      DOM.simulatorView.classList.toggle(
        "hidden",
        !isSimulator
      );
    }

    if (
      DOM.adminView
    ) {

      DOM.adminView.classList.toggle(
        "hidden",
        !isAdmin
      );
    }

    if (
      DOM.messagesView
    ) {

      DOM.messagesView.classList.toggle(
        "hidden",
        !isMessages
      );
    }


    /* -------------------------------------------------------
       BUTTONS
       ------------------------------------------------------- */

    if (
      DOM.ordersTabButton
    ) {

      DOM.ordersTabButton.classList.toggle(
        "active",
        isOrders
      );
    }

    if (
      DOM.simulatorTabButton
    ) {

      DOM.simulatorTabButton.classList.toggle(
        "active",
        isSimulator
      );
    }

    if (
      DOM.adminTabButton
    ) {

      DOM.adminTabButton.classList.toggle(
        "active",
        isAdmin
      );
    }

    if (
      DOM.messagesTabButton
    ) {

      DOM.messagesTabButton.classList.toggle(
        "active",
        isMessages
      );
    }


    /* -------------------------------------------------------
       SIMULATOR
       ------------------------------------------------------- */

    if (isSimulator) {

      setTimeout(
        () => {

          if (
            !SimulatorModule.isValidPhone(
              SimulatorModule.getPhone()
            )
          ) {

            SimulatorModule.focusPhone();

          } else {

            SimulatorModule.focusMessage();
          }

        },
        50
      );
    }


    /* -------------------------------------------------------
       ADMIN
       ------------------------------------------------------- */

    if (isAdmin) {

      setTimeout(
        () => {

          if (
            !AdminModule.initialized
          ) {

            AdminModule.init();
          }

          AdminModule.updatePeriodLabel();

          AdminModule.fetchDashboard();

        },
        50
      );
    }


    /* -------------------------------------------------------
       MENSAGENS
       ------------------------------------------------------- */

    if (isMessages) {

      setTimeout(
        () => {

          if (
            !MessagesModule.initialized
          ) {

            MessagesModule.init();
          }

          MessagesModule.fetchMessages();

        },
        50
      );
    }


    refreshIcons();
  },


  /* ---------------------------------------------------------
     EVENTS
     --------------------------------------------------------- */

  setupEvents() {

    if (
      DOM.ordersTabButton
    ) {

      DOM.ordersTabButton.addEventListener(
        "click",
        () =>
          this.activate(
            "orders"
          )
      );
    }

    if (
      DOM.simulatorTabButton
    ) {

      DOM.simulatorTabButton.addEventListener(
        "click",
        () =>
          this.activate(
            "simulator"
          )
      );
    }

    if (
      DOM.adminTabButton
    ) {

      DOM.adminTabButton.addEventListener(
        "click",
        () =>
          this.activate(
            "admin"
          )
      );
    }

    if (
      DOM.messagesTabButton
    ) {

      DOM.messagesTabButton.addEventListener(
        "click",
        () =>
          this.activate(
            "messages"
          )
      );
    }
  },


  /* ---------------------------------------------------------
     INIT
     --------------------------------------------------------- */

  init() {

    this.setupEvents();

    this.activate(
      "orders"
    );
  },
};


/* =========================================================
   SETTINGS MODULE
   ========================================================= */

const SettingsModule = {

  defaultAutoRefresh:
    8000,


  open() {

    if (
      !DOM.settingsOverlay
    ) {

      return;
    }

    this.load();

    DOM.settingsOverlay.classList.remove(
      "hidden"
    );

    setTimeout(
      () => {

        DOM.apiBaseInput?.focus();

      },
      50
    );

    refreshIcons();
  },


  close() {

    if (
      !DOM.settingsOverlay
    ) {

      return;
    }

    DOM.settingsOverlay.classList.add(
      "hidden"
    );
  },


  load() {

    const savedApiBase =
      localStorage.getItem(
        "barJaumApiBase"
      );

    const savedAutoRefresh =
      localStorage.getItem(
        "barJaumAutoRefresh"
      );

    if (
      DOM.apiBaseInput
    ) {

      DOM.apiBaseInput.value =
        savedApiBase ??
        OrdersModule.apiBase ??
        "";
    }

    if (
      DOM.autoRefreshInput
    ) {

      DOM.autoRefreshInput.value =
        savedAutoRefresh ??
        OrdersModule.autoRefreshInterval ??
        this.defaultAutoRefresh;
    }
  },


  save() {

    const apiBase =
      normalizeApiBase(
        DOM.apiBaseInput?.value ||
        ""
      );

    let autoRefresh =
      Number(
        DOM.autoRefreshInput?.value
      );

    if (
      !Number.isFinite(
        autoRefresh
      ) ||
      autoRefresh < 1000
    ) {

      autoRefresh =
        this.defaultAutoRefresh;
    }

    localStorage.setItem(
      "barJaumApiBase",
      apiBase
    );

    localStorage.setItem(
      "barJaumAutoRefresh",
      String(
        autoRefresh
      )
    );

    OrdersModule.apiBase =
      apiBase;

    OrdersModule.autoRefreshInterval =
      autoRefresh;

    SimulatorModule.apiBase =
      apiBase;

    SimulatorModule.updateEndpoint();

    OrdersModule.stopAutoRefresh();

    OrdersModule.startAutoRefresh();

    this.close();

    OrdersModule.fetchOrders();


    if (
      TabsModule.currentTab ===
      "admin"
    ) {

      AdminModule.fetchDashboard();
    }


    if (
      TabsModule.currentTab ===
      "messages"
    ) {

      MessagesModule.fetchMessages();
    }
  },


  setupEvents() {

    if (
      DOM.settingsButton
    ) {

      DOM.settingsButton.addEventListener(
        "click",
        () =>
          this.open()
      );
    }

    if (
      DOM.closeSettingsButton
    ) {

      DOM.closeSettingsButton.addEventListener(
        "click",
        () =>
          this.close()
      );
    }

    if (
      DOM.settingsBackdrop
    ) {

      DOM.settingsBackdrop.addEventListener(
        "click",
        () =>
          this.close()
      );
    }

    if (
      DOM.saveSettingsButton
    ) {

      DOM.saveSettingsButton.addEventListener(
        "click",
        () =>
          this.save()
      );
    }
  },


  init() {

    const savedApiBase =
      localStorage.getItem(
        "barJaumApiBase"
      );

    const savedAutoRefresh =
      localStorage.getItem(
        "barJaumAutoRefresh"
      );

    OrdersModule.apiBase =
      normalizeApiBase(
        savedApiBase ??
        API_CONFIG.baseUrl
      );

    OrdersModule.autoRefreshInterval =
      Number(
        savedAutoRefresh ??
        this.defaultAutoRefresh
      );

    if (
      !Number.isFinite(
        OrdersModule.autoRefreshInterval
      ) ||
      OrdersModule.autoRefreshInterval <
        1000
    ) {

      OrdersModule.autoRefreshInterval =
        this.defaultAutoRefresh;
    }

    SimulatorModule.apiBase =
      OrdersModule.apiBase;

    this.setupEvents();
  },
};


/* =========================================================
   GLOBAL KEYBOARD EVENTS
   ========================================================= */

document.addEventListener(
  "keydown",
  (event) => {

    if (
      event.key !==
      "Escape"
    ) {

      return;
    }


    if (
      DOM.orderModal &&
      !DOM.orderModal.classList.contains(
        "hidden"
      )
    ) {

      OrdersModule.closeOrderModal();

      return;
    }


    if (
      DOM.conversationModal &&
      !DOM.conversationModal.classList.contains(
        "hidden"
      )
    ) {

      MessagesModule.closeConversation();

      return;
    }


    if (
      DOM.settingsOverlay &&
      !DOM.settingsOverlay.classList.contains(
        "hidden"
      )
    ) {

      SettingsModule.close();
    }
  }
);


/* =========================================================
   APPLICATION BOOTSTRAP
   ========================================================= */

document.addEventListener(
  "DOMContentLoaded",
  async () => {

    try {

      /*
       * 1. Configuração
       */

      SettingsModule.init();


      /*
       * 2. Simulator
       */

      SimulatorModule.init();


      /*
       * 3. Administrativo
       */

      AdminModule.init();


      /*
       * 4. Mensagens
       */

      MessagesModule.init();


      /*
       * 5. Tabs
       */

      TabsModule.init();


      /*
       * 6. Orders
       */

      await OrdersModule.init();


      /*
       * 7. Ícones
       */

      refreshIcons();


      console.log(
        "[Bar do Jaum] Aplicação inicializada."
      );

    } catch (error) {

      console.error(
        "[Bar do Jaum] Erro durante inicialização:",
        error
      );
    }
  }
);