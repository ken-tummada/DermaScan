//
//  NavigationGesture.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import UIKit

extension UINavigationController {
    private static var gestureKey = ObjectIdentifier(UINavigationController.self)

    open override func viewDidLoad() {
        super.viewDidLoad()
        enableSwipeBackGesture()
    }

    func enableSwipeBackGesture() {
        guard let interactivePopGestureRecognizer = self.interactivePopGestureRecognizer,
              let gestureView = interactivePopGestureRecognizer.view else {
            return
        }

        let panGesture = UIPanGestureRecognizer(target: interactivePopGestureRecognizer.delegate, action: Selector(("handleNavigationTransition:")))
        gestureView.addGestureRecognizer(panGesture)

        objc_setAssociatedObject(self, &UINavigationController.gestureKey, panGesture, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
    }
}
