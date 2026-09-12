-- 1. Cria a função que faz a baixa no estoque quando o status for APPROVED
CREATE OR REPLACE FUNCTION delivery.fn_debito_estoque_aprovacao()
RETURNS TRIGGER AS $$
BEGIN
    -- Dispara se o status for alterado para 'APPROVED' (ou inserido diretamente como 'APPROVED')
    IF NEW.status = 'APPROVED' AND (OLD.status IS NULL OR OLD.status <> 'APPROVED') THEN
        
        -- Subtrai do estoque os produtos correspondentes aos itens do pedido
        UPDATE delivery.products p
        SET stock_quantity = p.stock_quantity - oi.quantity
        FROM delivery.order_items oi
        WHERE oi.order_id = NEW.id
          AND oi.product_id = p.id;
          
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Remove a trigger caso ela já exista para evitar duplicidade
DROP TRIGGER IF EXISTS trg_debito_estoque_aprovacao ON delivery.orders;

-- 3. Cria a trigger na tabela orders
CREATE TRIGGER trg_debito_estoque_aprovacao
AFTER INSERT OR UPDATE OF status ON delivery.orders
FOR EACH ROW
EXECUTE FUNCTION delivery.fn_debito_estoque_aprovacao();
